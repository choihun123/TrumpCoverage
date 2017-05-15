import sys
from json import loads

from pymongo import MongoClient

client = MongoClient()
db = client.trumpBak

def store_data_in_mongo(filename):
    collection_name = filename.split('_')[0]
    collection = getattr(db, collection_name)
    stored_articles = list(collection.find())
    stored_urls = set()
    for article in stored_articles:
        canonical_url = article.get('canonicalUrl', None)
        if canonical_url is None:
            canonical_url = article.get('canonical', None)
            if canonical_url is None:
                continue
            else:
                canonical_url = canonical_url[0]['href']
        stored_urls.add(canonical_url)
        
    with open(filename) as fp:
        data = loads(fp.read())        

    new_data = []
    for article in data:        
        canonical_url = article.get('canonicalUrl', None)
        if canonical_url is None:
            canonical_url = article.get('canonical', None)
            if canonical_url is None:
                continue
            else:
                canonical_url = canonical_url[0]['href']
                
        if canonical_url in stored_urls:
            continue
        article['newspaper_article_text'] = None
        new_data.append(article)
            

    collection.insert_many(new_data)
    return len(new_data)

def main():
    filename = sys.argv[1]
    print store_data_in_mongo(filename), 'records stored'

if __name__ == '__main__':
    main()
    


