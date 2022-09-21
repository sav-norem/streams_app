from audioop import avg
import redis
import collections
import sys

STREAM_KEY = 'low_health_good_reviews'
CONSUMER_GROUP_NAME = 'notifications'
CONSUMER_NAME = sys.argv[1]

r = redis.Redis(decode_responses=True)

try:
    r.xgroup_create(STREAM_KEY, CONSUMER_GROUP_NAME, '0', mkstream=True)
except:
    print("group exists")

while True:
    response = r.xreadgroup(CONSUMER_GROUP_NAME, CONSUMER_NAME, {STREAM_KEY: '>'}, count=1, block=5000)
    if len(response) > 0:
        # {'restaurant': name, 'health_score': score, 'avg_review': avg_rating}
        review = response[0]
        current_review_details = review[1][0][1]
        name = current_review_details['restaurant']
        score = int(current_review_details['health_score'])
        avg_review = int(current_review_details['avg_review'])