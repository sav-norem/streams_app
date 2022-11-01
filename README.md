# streams_app

## tl;dr
This app produces streams of reviews (currently ratings for restuarants and their health scores) and does some processing. If a highly rated restaurant gets a terrible health score, it publishes a messages to all the subsribers. There is also a top-k structure holding the most commonly used words in high/low/medium reviews for each restaurant. The data in the food trucks JSON gets translated into Redis Geospatial keys and can be used to find food trucks near given coordinates.

## Steps to Run
0. python3 -m pip install -r requirements.txt
1. python3 parse_trucks.py
2. python3 produce_health_reviews.py
3. python3 producer.py
4. python3 consumer_group.py {name_of_consumer}
5. python3 low_health_group.py {name_of_consumer}
6. python3 text_parse_group.py {name_of_consumer}
7. uvicorn main:app --reload

## Streams
Currently this project has a few streams being produced. The first round are 1-5 "star" reviews and 1-100 point health reviews. Those are then processed by our first consumer group. From there they get put on new streams, for high (4-5), medium (3), and low (1-2) star reviews. Those streams are processed and have a top-k structure keeping track of the top words used in each bucket for each restaurant - with generic stop words being taken out.

### Files
producer.py: A file that generates 1-5 star reviews (sometimes) with a basic text review (ie "great"). It also produces indices for each restaurant_rating and keeps track of how many of each "star" reviews each restaurant gets. Can be easily modified to accept reviews from users instead. 

produce_health_review.py: A file that generates a 1-100 health score for the same list of restaurants as producer.py

consumer.py: A starter consumer - more of a test than anything.

consumer_group.py: Reads off both the first round streams that are produced - adds them to the appropriate secondary streams, along with updating a sorted set with the average stars for each restaurant. Ignores "questionable" reviews which is currently pretty arbitrary. Adds high review + low health score to a new stream.

text_parse_group.py: Parses out common stop words and adds more meaningful words from each review to the appropriate top-k structure.

## Pub/Sub
When a really well regarded restaurant fails their health evaluation (which happens quite a bit in our random producer) we want to make sure people know!

### Files
low_health_group.py: Publishes a message of "{average star review}-Star restaurant {name} recieves a {health score} health rating!}

## Geo and OM

By using the [geopy library](https://geopy.readthedocs.io/en/stable/) we can use the address a food truck gives us (thanks [Justin](https://twitter.com/JustCastilla)) to get their longitude and latitude coordiantes. From there we add it as a geo index, using the same pk as the OM object we created so that we can later search for it. We're currently using an OM model to store and query the food truck data.

### Files
parse_trucks.py: Parses the food trucks JSON file, asks for the lat and lon for each given address, and saves the fields we want as an OM object in Redis. Adds the geo index for each truck using the pk from OM as the name to attempt making later searches easier.

truck_model.py: The model definition.


