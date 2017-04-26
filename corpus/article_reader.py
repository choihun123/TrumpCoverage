# usage: python article_reader.py json/nytimes_trump.json
import json
from nltk.sentiment.vader import SentimentIntensityAnalyzer
from nltk import tokenize
import sys

# take in news outlet json file
file_name = sys.argv[1]
with open(file_name) as data_file:    
    outlet = json.load(data_file)

# look at each sentence and judge the overall sentiment
sid = SentimentIntensityAnalyzer()
for news_page in outlet:
    page_text = news_page['newspaper_article_text']
    sentence_list = tokenize.sent_tokenize(page_text)
    for sentence in sentence_list:
        if "Trump" not in sentence:
            continue
        print sentence
        ss = sid.polarity_scores(sentence)
        for k in sorted(ss):
            print "{0}: {1}, ".format(k, ss[k]),
        print ""