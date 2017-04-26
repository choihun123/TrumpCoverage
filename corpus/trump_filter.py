# usage: python trump_filter.py json/nytimes.json
from glob import glob
import json

# take in news outlet json file
files = glob("json/*.json")
for file_name in files:
    # skip already filtered files
    if "trump" in file_name:
        continue

    with open(file_name) as data_file:    
        outlet = json.load(data_file)

    # go through all the URLs and look for Trump in the body
    filtered = []
    for news_page in outlet:
        page_text = news_page['newspaper_article_text']
        if "title" in news_page: # skips missing title errors
            page_title = news_page['title']
        else:
            page_title = ""
        if page_text == -1: # skips body text errors
            continue

        # look in title and body text
        if "President Trump" in page_text or "POTUS" in page_text \
            or "President Donald Trump" in page_text \
            or "President Trump" in page_title or "POTUS" in page_title \
            or "President Donald Trump" in page_title:
            filtered.append(news_page)

    # save the new filtered json file
    with open(file_name.replace(".json", "_trump.json"), 'w') as outfile:
        json.dump(filtered, outfile)