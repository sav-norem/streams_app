from flask import Flask, request
import redis
from truck_model import Vendor

app = Flask(__name__)
r = redis.Redis(decode_responses=True)

#@app.route("/<lon>/<lat>")
#def search_near_me(
lon=-122.256051
lat=37.820791
results = r.geosearch(name='truck_locations', longitude=lon, latitude=lat, radius=8050)
r.pipeline()
for res in results:
    Vendor.find(str(Vendor.pk) == res)
#print(results)
