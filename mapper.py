from types import SimpleNamespace
from models import Asteroid
import json


def map_asteroid(data, date_key) -> Asteroid:
    dumps = json.dumps(data)
    x = json.loads(dumps, object_hook=lambda d: SimpleNamespace(**d))
    return Asteroid(
        id=x.id,
        name=x.name,
        date=date_key,
        miss_distance_in_kilometers=x.estimated_diameter.kilometers.estimated_diameter_min)
