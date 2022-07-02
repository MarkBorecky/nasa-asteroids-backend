from dataclasses import dataclass
from pickle import TRUE
import json
from types import SimpleNamespace
# from fastapi import FastAPI
# from urllib import request
from datetime import date

import requests

# app = FastAPI()

url = "https://api.nasa.gov/neo/rest/v1/feed"

parameters = {
    "start_date": "2022-07-01",
    "end_date": "2022-07-07",
    "api_key": "pfvOZFYKGQOKTcMQRuVBHQXJjA3dr7qLYtnXmkN1"
}

headers = {
    "Accepts": "application/json"
}


@dataclass(frozen=TRUE)
class Asteroid:
    id: str
    name: str
    date: date
    miss_distance_in_kilometers: float


# https://api.nasa.gov/neo/rest/v1/feed?start_date=2022-07-01&end_date=2022-07-07&api_key=pfvOZFYKGQOKTcMQRuVBHQXJjA3dr7qLYtnXmkN1
# @app.get("/api/v1/asteroids")
def fetch_asteroids() -> [Asteroid]:
    # id, date, name, distance, miss_distance.kilometers

    json = requests.get(url, params=parameters, headers=headers).json()
    nearest_objects = json.get('near_earth_objects')
    result = []
    for date_key in nearest_objects:
        for obj in nearest_objects[date_key]:
            result.append(map_asteroid(obj, date_key))
    return result


def map_asteroid(data, date_key) -> Asteroid:
    dumps = json.dumps(data)
    x = json.loads(dumps, object_hook=lambda d: SimpleNamespace(**d))
    return Asteroid(
        id=x.id,
        name=x.name,
        date=date_key,
        miss_distance_in_kilometers=x.estimated_diameter.kilometers.estimated_diameter_min)

# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    asteroids = fetch_asteroids()

