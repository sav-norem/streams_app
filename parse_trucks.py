from cmath import nan
import json
import numpy as np
from truck_model import Vendor
import asyncio
from aredis_om import Migrator
from geopy.geocoders import Nominatim
import redis

# parses the food truck data - gets longitude and latitude when available

r = redis.Redis(
    host='localhost', 
    port=6379, 
    db=0, 
    decode_responses=True
)

with open('food_trucks.json') as f:
    trucks = json.load(f)

locator = Nominatim(user_agent="savannahs_stream_app")

truck_list = []

trucks = trucks['data']['vendors']
for truck in trucks:
    if not truck['vendor_info']:
        continue
    else:
        truck_data = {}
        truck_data['cuisines'] = truck['cuisines']
        truck_data['id'] = truck['id']
        truck_data['name'] = truck['name']
        truck_data['primary_cuisine'] = truck['primary_cuisine']

        str_address = str(truck['vendor_info']['address']) + ", " + str(truck['vendor_info']['city']) + ", " + str(truck['vendor_info']['state'])
        location = locator.geocode(str_address, timeout=500)
        if location:
            truck_data['vendor_lat'] = location.latitude
            truck_data['vendor_lon'] = location.longitude
            r.geoadd('truck_locations', (location.longitude, location.latitude, truck['name']))
            n = truck['name']
            new_truck = Vendor(**truck_data)
            new_truck.save()
            truck_list.append(n)
            r.lpush('restaurant_list', truck['name'])
        else:
            pass

for food_truck in truck_list:
    n = len(r.geosearch('truck_locations', member=food_truck, radius=2, unit='mi'))
    r.zadd('num_close', {food_truck: n})

asyncio.run(Migrator().run())