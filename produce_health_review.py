import redis
import random
import time

restaurants = [
    "savannah's spot",
    "justin's joint",
    "guy's gastropub",
    "conrad's indian and soul food",
    "simon's soul food"
]


STREAM_KEY = 'health_ratings'

r = redis.Redis(decode_responses=True)

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