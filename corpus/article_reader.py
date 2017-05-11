# usage: python article_reader.py json/nytimes_trump.json
from collections import OrderedDict
import datetime
import json
import matplotlib.pyplot as plt
from nltk.sentiment.vader import SentimentIntensityAnalyzer
from nltk import tokenize
import numpy as np
from scipy import stats
from spacy.en import English
import sys
import time

# take in news outlet json file
file_name = sys.argv[1]
with open(file_name) as data_file:    
    outlet = json.load(data_file)

# initialize parser
parser = English()

# look at each sentence and judge the overall sentiment
sid = SentimentIntensityAnalyzer()

# plotting axes
x = []
x_ticks = []
y = []
daily_count = {}
daily_average = {}

for news_page in outlet:
    page_text = news_page['newspaper_article_text']
    sentence_list = tokenize.sent_tokenize(page_text)
    average_sentiment = 0.0
    count = 0

    for sentence in sentence_list:
        # filter sentences that don't have Trump in them
        if "Trump" not in sentence:
            continue

        # filter out sentences that don't have Trump as the subject
        parsedData = parser(sentence)
        sub_toks = [tok for tok in parsedData if (tok.dep_ == "nsubj") ]
        for tok in sub_toks:
            if "Trump" in tok.orth_ or "POTUS" in tok.orth_:
                #print sentence
                ss = sid.polarity_scores(sentence)
                average_sentiment += ss['compound']
                count += 1
    if count is not 0:
        date = datetime.datetime.fromtimestamp(news_page['published']/1000).strftime('%Y/%m/%d')
        if date not in daily_count:
            daily_count[date] = 1
            daily_average[date] = average_sentiment/count
        else:
            daily_count[date] += 1
            daily_average[date] += (average_sentiment/count)

# sort by date order for convenience
ordered_averages = OrderedDict(sorted(daily_average.items()))
for date,sentiments in ordered_averages.iteritems():
    sentiments /= daily_count[date]
    x.append(time.mktime(datetime.datetime.strptime(date, "%Y/%m/%d").timetuple()))
    y.append(sentiments)
    x_ticks.append(date)

# set up matplotlib
np_x = np.array(x)
np_y = np.array(y)
np_x_ticks = np.array(x_ticks)
fig = plt.figure(1, figsize=(20,10))
plt.xticks(x, x_ticks, rotation=90)
title_index = file_name.find("_trump.json")
title = file_name[5:title_index] + " sentiment analysis"
plt.title(title)

# linear best fit
slope, intercept, r_value, p_value, std_err = stats.linregress(np_x, np_y)
line = slope*np_x+intercept

# plot
plt.plot(x, y, "o--", x, line)
plt.show()
