import redis
import random
import time

STREAM_KEY = 'reviews'

r = redis.Redis(decode_responses=True)

while True:
    print("Restaurant name: ")
    name = input()
    print("Rating (1-5):")
    rating = int(input())

    review = {
        "restaurant": name,
        "rating": rating
    }

    review_id = r.xadd(STREAM_KEY, review)
    print(f"Created rating {review_id}:")