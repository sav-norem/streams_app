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

low_reviews = ['bleh', 'poor', 'mediocre', 'meh']
mid_reviews = ['average', 'fine', 'meets expectations']
high_reviews = ['great', 'excellent', 'wonderful']


STREAM_KEY = 'reviews'

r = redis.Redis(decode_responses=True)

while True:
    try:
        name = random.choice(restaurants)
        rating = random.randint(1,5)
        if rating <= 2:
            text_review = random.choice(low_reviews)
        elif rating == 3:
            text_review = random.choice(mid_reviews)
        else:
            text_review = random.choice(high_reviews)

        review = {
            "restaurant": name,
            "rating": rating,
            "text_review": text_review
        }

        # Generate a unique key with restaurantName_rating_<actual_rating> and increase its value by 1.If no key exists a default of 1 will be added else existing will be updated
        r.hincrby(name+"_"+"rating_"+rating,1)

        review_id = r.xadd(STREAM_KEY, review)
        print(f"Created rating {review_id}:")
    
    except:
        print("could not add to stream")

    time.sleep(random.randint(1, 5))