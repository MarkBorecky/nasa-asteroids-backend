from datetime import datetime

import asteroid_servise
from models import DateRange

if __name__ == '__main__':
    print(asteroid_servise.fetch_asteroids_between(DateRange(datetime(2022, 7, 1), datetime(2022, 7, 7))))
