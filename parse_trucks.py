from cmath import nan
import json
import numpy as np
from truck_model import Vendor
import asyncio
from aredis_om import Migrator
from geopy.geocoders import Nominatim
import redis

#truck_data = {
#    cuisines: List[str] = Field(index=True)
#    events: List[str] = Field(index=True)
#    id: str = Field(index=False)
#    name: str = Field(index=True, full_text_search=True)
#    primary_cuisine: str = Field(index=True)
#    vendor_lon: decimal
#    vendor_lat: decimal
#}

r = redis.Redis(
    host='localhost', 
    port=6379, 
    db=0, 
    decode_responses=True
)

with open('food_trucks.json') as f:
    trucks = json.load(f)

locator = Nominatim(user_agent="savannahs_stream_app")

trucks = trucks['data']['vendors']
for truck in trucks:
    if not truck['vendor_info']:
        continue
    else:
        truck_data = {}
        truck_data['cuisines'] = truck['cuisines']
        truck_data['events'] = truck['events']
        truck_data['id'] = truck['id']
        truck_data['name'] = truck['name']
        truck_data['primary_cuisine'] = truck['primary_cuisine']

        str_address = str(truck['vendor_info']['address']) + ", " + str(truck['vendor_info']['city']) + ", " + str(truck['vendor_info']['state'])
        print(str_address)
        location = locator.geocode(str_address, timeout=500)
        if location:
            truck_data['vendor_lat'] = location.latitude
            truck_data['vendor_lon'] = location.longitude
        
        else:
            continue

        new_truck = Vendor(**truck_data)
        new_truck.save()
        geo_name = new_truck.pk
        r.geoadd('truck_locations', (location.longitude, location.latitude, geo_name))

asyncio.run(Migrator().run())