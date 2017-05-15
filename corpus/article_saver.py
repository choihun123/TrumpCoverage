import sys
from threading import Thread
from multiprocessing import Process

import newspaper
from pymongo import MongoClient

import feedly_getter

NO_CANONICAL = -1
NUM_THREADS = 4

MONGO_HOST = '140.180.188.53'
MONGO_PORT = 27017

OUTLET = sys.argv[1]

def get_text_for_article(item):
    canonical_url = item.get('canonicalUrl', None)

    if canonical_url is None:
        canonical_url = item.get('canonical', None)
        if canonical_url is None:
            print 'no url'
            return NO_CANONICAL
        else:
            canonical_url = canonical_url[0]['href']
            
    article = newspaper.Article(canonical_url)
    article.download()
    article.parse()
    return article.text

def thread_get_articles():
    client = MongoClient(MONGO_HOST, MONGO_PORT)
    db = client.trumpBak
    collection = getattr(db, OUTLET)
    article = collection.find_one_and_delete({'newspaper_article_text': None})
    while article is not None:
        text = get_text_for_article(article)
        article['newspaper_article_text'] = text
        collection.insert(article)
        article = collection.find_one_and_delete({'newspaper_article_text': None})

def save_outlet_articles():
    threads = []
    for _ in xrange(NUM_THREADS): 
        thread = Process(target=thread_get_articles)
        thread.start()
        threads.append(thread)
        
    for thread in threads:
        thread.join()
save_outlet_articles()
