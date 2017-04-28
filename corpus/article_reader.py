# usage: python article_reader.py json/nytimes_trump.json
import json
from nltk.sentiment.vader import SentimentIntensityAnalyzer
from nltk import tokenize
from spacy.en import English
import sys

# take in news outlet json file
file_name = sys.argv[1]
with open(file_name) as data_file:    
    outlet = json.load(data_file)

# initialize parser
parser = English()

# look at each sentence and judge the overall sentiment
sid = SentimentIntensityAnalyzer()
total_sentiment = 0.0
total_count = 0

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
            if tok.orth_ == "Trump":
                #print sentence
                ss = sid.polarity_scores(sentence)
                average_sentiment += ss['compound']
                total_sentiment += ss['compound']
                count += 1
                total_count += 1
                # prints out the different sentiments 
                # for key in sorted(ss):
                #     print "{0}: {1}, ".format(key, ss[key]),
                # print "\n"
    if count is not 0:
        print news_page['canonicalUrl']
        print "Article sentiment average: " + str(average_sentiment/count)
# print "Outlet sentiment average: " + str(total_sentiment/total_count)