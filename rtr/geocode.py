import time
import os

import requests
import geojson
import shapely

api_key = os.environ['ORS_KEY']


def geocode(text):
    if type(text) != float:
        try:
            time.sleep(60/90)
            r = requests.get(f"https://api.openrouteservice.org/geocode/search?api_key={api_key}&text={text}")
            geo = geojson.loads(r.content)
            geo = geo['features'][0]['geometry']
            geo = shapely.geometry.shape(geo)
            return shapely.to_wkt(geo)
        except Exception:
            print(f"Geocoding failed for {text}")
            return None
    return None
