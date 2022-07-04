import unittest
from collections import defaultdict
from datetime import date
from mapper import map_asteroid
from models import DateRange, Asteroid, AsteroidToFetch, DateRangeCollector
from nasa_api_client import fetch_asteroids_from_nasa


redis_mock = {}


def check_cache(day):
    return redis_mock.get(day, AsteroidToFetch(day))


def collect_ranges(to_fetch: [AsteroidToFetch]) -> [DateRange]:
    collector = DateRangeCollector()
    for fetch in to_fetch:
        collector.add(fetch.date)
    return collector.finish()


def get_nearest_asteroid(asteroids: [Asteroid], date: date):
    mapped_asteroids = (map_asteroid(a, date) for a in asteroids)
    return collect_the_closest_asteroids_by_date(mapped_asteroids)


def fetch_from_api(date_range: DateRange) -> {Asteroid}:
    objects = fetch_asteroids_from_nasa(date_range).get('near_earth_objects')
    result = {}
    for date_key in objects:
        asteroid = get_nearest_asteroid(objects[date_key], date_key).get(date_key)
        result.update({date_key: asteroid})
    return result


def save(asteroids_by_range: [{Asteroid}]):
    result = []
    for asteroids in asteroids_by_range:
        for key in asteroids.keys():
            asteroid = asteroids[key]
            redis_mock.update({key: asteroid})
            result.append(asteroid)
    return result


def is_asteroid(a):
    return type(a).__name__ == 'Asteroid'


def fetch_asteroids_between(date_range: DateRange) -> [Asteroid]:
    result = list(check_cache(day) for day in date_range.days())
    to_fetch = list(filter(lambda a: is_to_fetch(a), result))
    ranges: [DateRange] = collect_ranges(to_fetch)
    # TODO invoke it parallel
    closest_fetched: [{Asteroid}] = (fetch_from_api(r) for r in ranges)
    cached = save(closest_fetched)
    old_result: [Asteroid] = list(filter(lambda a: is_asteroid(a), result))
    return old_result + cached


def is_to_fetch(a):
    return type(a).__name__ == 'AsteroidToFetch'


def map_elements_by(elements, func_key) -> dict[Asteroid]:
    asteroid_dict = defaultdict(list)
    for a in elements:
        asteroid_dict[func_key(a)].append(a)
    return asteroid_dict


def pick_the_closest_asteroids_per_date(asteroids: [[Asteroid]]) -> [Asteroid]:
    return list(min(sublist, key=lambda asteroid: asteroid.miss_distance_in_kilometers) for sublist in asteroids)


def collect_the_closest_asteroids_by_date(asteroids):
    temp = map_elements_by(asteroids, lambda asteroid: asteroid.date)
    return dict(get_value(key, temp, lambda asteroid: asteroid.miss_distance_in_kilometers) for key in temp.keys())


def get_value(key, dictionary, func):
    return key, min(dictionary.get(key), key=func)


def is_asteroid_to_fetch(obj):
    return type(obj).__name__, 'AsteroidToFetch'
