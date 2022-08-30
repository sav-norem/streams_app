from audioop import avg
import redis
import collections
import sys

review_dict = collections.defaultdict(list)

STREAM_KEY = 'reviews'
CONSUMER_GROUP_NAME = 'staff'
CONSUMER_NAME = sys.argv[1]

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
            rating = int(current_review_details['rating'])
            r.lpush(name, rating)
            sum_reviews = sum([int(x) for x in r.lrange(name, 0, -1)])
            num_reviews = r.llen(name)
            avg_rating = sum_reviews / num_reviews
            r.zadd('avg_reviews', {name: avg_rating})
            print(r.zscore('avg_reviews', name))
        else:
            print("no jobs in response")
    
    except:
        print("there's been an error") 