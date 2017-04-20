import sys
from threading import Thread

from pymongo import MongoClient

import article_saver

OUTLET = sys.argv[1]

def label_articles():
    client = MongoClient(article_saver.MONGO_HOST, article_saver.MONGO_PORT)
    db = client.trumpArticles
    collection = getattr(db, OUTLET)
    retreived_articles_query = {'$and': [{'newspaper_article_text': {'$ne': None}}, {'newspaper_article_text':  {'$ne': -1}}, {'article_label': {'$ne': True}}]}
    
    article = collection.find_one_and_delete(retreived_articles_query)
    while article is not None:
        article['article_label'] = 'Trump' in article['newspaper_article_text'] or 'trump' in article['newspaper_article_text']
        collection.insert(article)
        article = collection.find_one_and_delete(retreived_articles_query)

threads = []
for _ in xrange(article_saver.NUM_THREADS):
    thread = Thread(target=label_articles)
    thread.start()
    threads.append(thread)

for thread in threads:
    thread.join()
