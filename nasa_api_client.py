import requests

from datetime import date

from models import DateRange

url = "https://api.nasa.gov/neo/rest/v1/feed"

api_key = "pfvOZFYKGQOKTcMQRuVBHQXJjA3dr7qLYtnXmkN1"


def get_params(start: date, end: date, key: str):
    return {
        "start_date": start,
        "end_date": end,
        "api_key": key
    }


headers = {
    "Accepts": "application/json"
}


def fetch_asteroids_from_nasa(date_range: DateRange):
    params = get_params(
        start=date_range.start,
        end=date_range.end,
        key=api_key
    )
    return requests.get(url, params=params, headers=headers).json()

