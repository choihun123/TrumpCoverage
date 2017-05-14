"""
Get lists of articles on site from feedly.

"""
import subprocess
import json

NUM_ARTICLE_REQS = 20
BASE_URL_0 = "https://feedly.com/v3/streams/contents?streamId=feed%2F{outlet_rss_url}&count=1000&ranked=newest&similar=true"
CONTINUATION_BASE = "&continuation="
BASE_URL_2 = "&ck=1492623749498&ct=feedly.desktop&cv=30.0.1320"
OUTPUT_FILENAME = "output.json"

GET_ARTICLES_SCRIPT_FILENAME = "get_articles.bash"

START_TSTAMP = "1484870399"
START_FEEDLY_TSTAMP = int(START_TSTAMP + "000")

END_TSTAMP = "1492905600"
END_FEEDLY_TSTAMP = int(END_TSTAMP + "000")


OUTLETS_AND_URLS = {
    "nytimes": "http%3A%2F%2Fwww.nytimes.com%2Fservices%2Fxml%2Frss%2Fnyt%2FHomePage.xml",
    "cnn": "http%3A%2F%2Frss.cnn.com%2Frss%2Fcnn_topstories.rss",
    "fox_news": "http%3A%2F%2Fwww.foxnews.com%2Fxmlfeed%2Frss%2F0%2C4313%2C0%2C00.rss",
    "huffington_post": "http%3A%2F%2Fwww.huffingtonpost.com%2Ffeeds%2Fverticals%2Fpolitics%2Findex.xml",
    "breitbart": "https%3A%2F%2Fwp.breitbart.com%2Ffeed%2Fatom%2F",
}

def feedly_tstamp_to_regular(feedly_tstamp_s):
    feedly_tstamp = feedly_tstamp[:-3]
    return feedly_tstamp

def get_articles_of_outlet(outlet_url):
    BASE_URL_1 = BASE_URL_0.format(outlet_rss_url=outlet_url)
    INITIAL_URL = BASE_URL_1 + BASE_URL_2
    BASE_CURL_CMD = 'curl "{url}"'
    curl_cmd = BASE_CURL_CMD.format(url=INITIAL_URL)
    all_items = []
    for _ in xrange(NUM_ARTICLE_REQS):
        with open(GET_ARTICLES_SCRIPT_FILENAME, 'w+') as get_articles_script_file:
            get_articles_script_file.write(curl_cmd)
        cmd = ["bash",  GET_ARTICLES_SCRIPT_FILENAME] # + " > " + OUTPUT_FILENAME
        output_s = subprocess.check_output(cmd)
        response = json.loads(output_s)
        continuation = response["continuation"]        
        url = BASE_URL_1 + CONTINUATION_BASE + continuation + BASE_URL_2
        curl_cmd = BASE_CURL_CMD.format(url=url)
        items = response["items"]
        print 'len_items', len(items)
        for item in items:
            if int(item['published']) < START_FEEDLY_TSTAMP:
                # import ipdb; ipdb.set_trace()
                print 'skipped early article'
                continue
                # break
            elif int(item['published']) > END_FEEDLY_TSTAMP:
                print 'skipped late article'
                continue
            all_items.append(item)
    return all_items

def save_article_lists(outlets_and_urls):
    for outlet, url in outlets_and_urls.iteritems():
        feedly_list = get_articles_of_outlet(url)
        filename = outlet + '_feedly_list_fixed.json'
        with open(filename, 'w+') as fp:
            fp.write(json.dumps(feedly_list))


def main():
    save_article_lists(OUTLETS_AND_URLS)

if __name__ == '__main__':
    main()
        
    
    
