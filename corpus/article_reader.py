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

def get_res_tokens(resolution_dict):
    tokens = resolution_dict['tokens']
    resolved_tokens = [token_resolution['to'] for token_resolution in tokens]
    return resolved_tokens

def get_res_token_by_idx(idx, res_dict):
    tokens = res_dict['tokens']
    for token in tokens:
        if token['idx'] == idx:
            return token['to']
        
    return None

def is_s_in_res_token(s, idx, res_dict):
    res_token = get_res_token_by_idx(idx, res_dict)
    if res_token is None:
        return False
    return s.lower() in res_token.lower()

# take in news outlet json file
file_name = sys.argv[1]
title = sys.argv[2]
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

for article_count, news_page in enumerate(outlet):
    date = datetime.datetime.fromtimestamp(news_page['published']/1000).strftime('%Y/%m/%d')
    _, m, d = date.split('/')
    m = int(m)
    d = int(d)
    if m == 1 and d == 19:
        continue # skip the 19th articles
    print 'article_count', article_count
    page_text = news_page['newspaper_article_text']
    resolutions = news_page['resolutions']
    sentence_list = tokenize.sent_tokenize(page_text)
    average_sentiment = 0.0
    count = 0

    if not resolutions:
        print 'no resolutions'
        continue
    for resolution_dict, sentence in zip(resolutions, sentence_list):
        # filter sentences that don't have Trump in them
        res_tokens = get_res_tokens(resolution_dict)
        should_continue = False
        if "Trump" not in sentence:
            should_continue = True
            resolved_tokens = get_res_tokens(resolution_dict)
            for resolved_token in resolved_tokens:
                if "Trump" in resolved_token:
                    should_continue = False
                    break
                elif "trump":
                    should_continue = False
                    break
                    
        if should_continue:
            continue
        
        # filter out sentences that don't have Trump as the subject
        parsedData = parser(sentence)
        idx_and_sub_toks = [(idx, tok) for idx, tok in enumerate(parsedData) if (tok.dep_ == "nsubj")]
        for idx, tok in idx_and_sub_toks:
            lower_orth = tok.orth_.lower()
            if "trump" in lower_orth or "potus" in lower_orth or is_s_in_res_token(lower_orth, idx, resolution_dict):
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
plot_title = title + " sentiment analysis"
plt.title(plot_title)

# linear best fit
slope, intercept, r_value, p_value, std_err = stats.linregress(np_x, np_y)
line = slope*np_x+intercept

# plot
plt.plot(x, y, "o--", x, line)
plt.show()
savefig(title)
