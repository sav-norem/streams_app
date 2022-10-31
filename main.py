from cmath import inf
from numpy import double
from fastapi import FastAPI
import redis
from truck_model import Vendor

app = FastAPI()
r = redis.Redis(decode_responses=True)

# the root page
@app.get("/")
async def root():
    return {"message": "Hello World"}

# four star+ avg reviews near a location
@app.get("/4star_near_me")
async def four_star_close(lon: double = -122.256051, lat: double = 37.820791, rad: int = 2):
    four_stars = r.zrangebyscore('avg_reviews', 4, +inf)
    near_me = r.geosearch(name='truck_locations', longitude=lon, latitude=lat, radius=5, unit='mi')
    four_near_me = set(four_stars).intersection(set(near_me))
    return {"four stars close": four_near_me}

# the number of restuarants near a location
@app.get("/number_near_me")
async def number_close(lon: double = -122.256051, lat: double = 37.820791, rad: int = 2):
    return {"number close": r.geosearchstore('trash', 'truck_locations', longitude=lon, latitude=lat, radius=rad, unit='mi') } 

# a list of restaurants near a location
@app.get("/near_me")
async def search_near_me(lon: double = -122.256051, lat: double = 37.820791):
    results = r.geosearch(name='truck_locations', longitude=lon, latitude=lat, radius=5, unit='mi')
    return ( {"trucks: ": len(results)} )

