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
    try:
        assert (rating in [1,2,3,4,5])
        print("leave a text review")
        text_review = input()

        review = {
            "restaurant": name,
            "rating": rating,
            "text_review": text_review
        }

        review_id = r.xadd(STREAM_KEY, review)
        print(f"Created rating {review_id}:")
    
    except:
        print("Not a 1-5 rating - try again")