import unittest
from datetime import datetime, date
import asteroid_servise
from models import DateRange, Asteroid


class IntegrationTest(unittest.TestCase):

    def test_fetch_asteroids_from_01_to_07_july(self):
        result = asteroid_servise.fetch_asteroids_between(DateRange(datetime(2022, 7, 1), datetime(2022, 7, 7)))

        expected = [
            Asteroid(
                    id='54136761',
                    name='(2021 GX7)',
                    date='2022-07-07',
                    miss_distance_in_kilometers=0.0119276525),
            Asteroid(
                    id='3776858',
                    name='(2017 OA)',
                    date='2022-07-06',
                    miss_distance_in_kilometers=0.2658),
            Asteroid(
                    id='3042555',
                    name='(2000 LG6)',
                    date='2022-07-05',
                    miss_distance_in_kilometers=0.0042126461),
            Asteroid(
                    id='3728229',
                    name='(2015 SG)',
                    date='2022-07-04',
                    miss_distance_in_kilometers=0.0139493823),
            Asteroid(
                    id='54194357',
                    name='(2021 RG6)',
                    date='2022-07-03',
                    miss_distance_in_kilometers=0.00437074),
            Asteroid(
                    id='3768021',
                    name='(2017 CP)',
                    date='2022-07-02',
                    miss_distance_in_kilometers=0.0096506147),
            Asteroid(
                    id='54224418',
                    name='(2021 WV1)',
                    date='2022-07-01',
                    miss_distance_in_kilometers=0.0052790403)
        ]
        self.assertEqual(result, expected)


if __name__ == '__main__':
    unittest.main()
