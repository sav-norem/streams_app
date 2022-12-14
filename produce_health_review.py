import redis
import random
import time

# produces fake health reviews for the same food trucks we're using everywhere

STREAM_KEY = 'health_ratings'

r = redis.Redis(decode_responses=True)

restaurants = r.lrange('restaurant_list', 0, -1)

while True:
    try:
        review = {
            "restaurant": random.choice(restaurants),
            "health_score": random.randint(1,100)
        }

        review_id = r.xadd(STREAM_KEY, review)
        print(f"Created rating {review_id}:")
    
    except:
        print("Could not add to stream")

    time.sleep(random.randint(1, 10))