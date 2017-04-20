import sys
from json import loads

from pymongo import MongoClient

client = MongoClient()
db = client.trump

def store_data_in_mongo(filename):
    collection_name = filename.split('_')[0]
    collection = getattr(db, collection_name)
    articles = collection.articles

    with open(filename) as fp:
        data = loads(fp.read())

    for article in data:
        article['newspaper_article_text'] = None

    articles = collection.insert_many(data)
    return len(data)

def main():
    filename = sys.argv[1]
    print store_data_in_mongo(filename), 'records stored'

if __name__ == '__main__':
    main()
    


