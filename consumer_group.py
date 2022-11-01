from audioop import avg
import redis
import collections
import sys

review_dict = collections.defaultdict(list)

STREAM1_KEY = 'reviews'
STREAM2_KEY = 'health_ratings'
CONSUMER_GROUP_NAME = 'staff'
CONSUMER_NAME = sys.argv[1]

r = redis.Redis(decode_responses=True)

# lessons learned: flagging if a review is questionable is tough
#       first reviews are extra tough because there's no baseline
#       should there be a minimum # of reviews before any get flagged?
# 
# def is_not_questionable_review(rating, name, text_review, review_id):
#    if rating > 3:
#        return True
#    else:
#        avg = r.zscore('avg_reviews', name)
#        if avg < 3: 
#            return True
#        if text_review == '':
#            r.xdel(STREAM1_KEY, review_id)
#            return False
#        else:
#            return True

def process_text_review(response):
    review = response[0]
    current_review_id = review[1][0][0]
    current_review_details = review[1][0][1]
    name = current_review_details['restaurant']
    rating = int(current_review_details['rating'])
    text_review = current_review_details['text_review']
    r.lpush(name, rating)
    sum_reviews = sum([int(x) for x in r.lrange(name, 0, -1)])
    num_reviews = r.llen(name)
    avg_rating = sum_reviews / num_reviews
    r.zadd('avg_reviews', {name: avg_rating})
    print(r.zscore('avg_reviews', name))

    if rating <= 2:
        print("adding low review")
        r.xadd('low_reviews', {'restaurant': name, 'text_review': text_review})
    elif rating == 3:
        print("adding mid review")
        r.xadd('mid_reviews', {'restaurant': name, 'text_review': text_review})
    else:
        print("adding high review")
        r.xadd('high_review', {'restaurant': name, 'text_review': text_review})

def process_health_review(response):
    review = response[0]
    current_review_details = review[1][0][1]
    name = current_review_details['restaurant']
    score = int(current_review_details['health_score'])
    if score < 71:
        avg_rating = r.zscore('avg_reviews', name)
        if avg_rating > 3.5:
            r.xadd('low_health_good_reviews', {'restaurant': name, 'health_score': score, 'avg_review': avg_rating})

try:
    r.xgroup_create(STREAM1_KEY, CONSUMER_GROUP_NAME, '0', mkstream=True)
except:
    print("group exists")

try:
    r.xgroup_create(STREAM2_KEY, CONSUMER_GROUP_NAME, '0', mkstream=True)
except:
    print("group exists")



while(True):
    try:    
        response = r.xreadgroup(CONSUMER_GROUP_NAME, CONSUMER_NAME, {STREAM1_KEY: '>'}, count=1, block=5000)
        if len(response) > 0:
            process_text_review(response)       
        else:
            print("no text reviews in response")

        response = r.xreadgroup(CONSUMER_GROUP_NAME, CONSUMER_NAME, {STREAM2_KEY: '>'}, count=1, block=5000)
        if len(response) > 0:
            process_health_review(response)
        else:
            print("no new health ratings in response")
    
    except:
        print("there's been an error")