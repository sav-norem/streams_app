from audioop import avg
from typing import Container
import redis
import collections
import sys
from nltk.corpus import stopwords

STREAM_KEY = sys.argv[1]
CONSUMER_GROUP_NAME = sys.argv[2]
CONSUMER_NAME = sys.argv[3]

r = redis.Redis(decode_responses=True)

try:
    r.xgroup_create(STREAM_KEY, CONSUMER_GROUP_NAME, '0', mkstream=True)
except:
    print("group exists")

while(True):
    try:
        response = r.xreadgroup(CONSUMER_GROUP_NAME, CONSUMER_NAME, {STREAM_KEY: '>'}, count=1, block=5000)
        if len(response) > 0:
            review = response[0]
            current_review_id = review[1][0][0]
            current_review_details = review[1][0][1]
            name = current_review_details['restaurant']
            desc = current_review_details['text_review']
            name_stream = f'{name}_{STREAM_KEY}'
            try:
                r.topk().reserve(name_stream, 5, 8, 7, .9)
            except:
                print(f"topk for {name_stream} already exists")
            list_desc = desc.split(" ")
            for word in list_desc:
                if word not in stopwords:
                    r.topk().add(name_stream, word)
                else:
                    continue
                
            print(r.topk().list(name_stream))

        else:
            print(f"no {STREAM_KEY} reviews to process")


    except:
        continue