import sys

from bson import json_util
from pymongo import MongoClient

OUTLET = sys.argv[1]
client = MongoClient()
db = client.trumpBak
collection = getattr(db, OUTLET)
data = [_ for _ in collection.find({})]

out_filename = OUTLET + '.json'
with open(out_filename, 'w+') as fp:
    fp.write(json_util.dumps([_ for _ in data]))
