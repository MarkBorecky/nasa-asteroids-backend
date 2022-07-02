import unittest
from datetime import date, datetime

import asteroid_servise
from models import DateRange, AsteroidToFetch, DateRangeCollector


class TestDataRangeUtilMethods(unittest.TestCase):

    def test_create_day_list(self):
        start = date(2022, 7, 1)
        end = date(2022, 7, 7)
        date_range = DateRange(start, end)
        self.assertEqual(date_range.days(),
                         [
                             datetime(2022, 7, 1, 0, 0),
                             datetime(2022, 7, 2, 0, 0),
                             datetime(2022, 7, 3, 0, 0),
                             datetime(2022, 7, 4, 0, 0),
                             datetime(2022, 7, 5, 0, 0),
                             datetime(2022, 7, 6, 0, 0),
                             datetime(2022, 7, 7, 0, 0)
                         ])

    def test_check_type(self):
        self.assertTrue(asteroid_servise.is_asteroid_to_fetch(AsteroidToFetch(date(2022, 7, 1))))

    def test_date_range_collector_should_return_one_range(self):
        collector = DateRangeCollector()
        collector.add(date(2022, 7, 1))
        collector.add(date(2022, 7, 2))
        result = collector.finish()
        self.assertEqual(result, [DateRange(datetime(2022, 7, 1, 0, 0), datetime(2022, 7, 2, 0, 0))])

    def test_date_range_collector_should_return_two_ranges(self):
        collector = DateRangeCollector()
        collector.add(datetime(2022, 7, 1, 0, 0))
        collector.add(datetime(2022, 7, 3, 0, 0))
        result = collector.finish()
        self.assertEqual(result,
                         [
                             DateRange(datetime(2022, 7, 1, 0, 0), datetime(2022, 7, 1, 0, 0)),
                             DateRange(datetime(2022, 7, 3, 0, 0), datetime(2022, 7, 3, 0, 0))
                         ])

    def test_fetching_collecting_ranges(self):
        # given
        to_fetch = [AsteroidToFetch(d) for d in DateRange(date(2022, 7, 1), date(2022, 7, 31)).days()]

        # when
        result = asteroid_servise.collect_ranges(to_fetch)

        # then
        self.assertEqual(result, [
            DateRange(datetime(2022, 7, 1, 0, 0), datetime(2022, 7, 7, 0, 0)),
            DateRange(datetime(2022, 7, 8, 0, 0), datetime(2022, 7, 14, 0, 0)),
            DateRange(datetime(2022, 7, 15, 0, 0), datetime(2022, 7, 21, 0, 0)),
            DateRange(datetime(2022, 7, 22, 0, 0), datetime(2022, 7, 28, 0, 0)),
            DateRange(datetime(2022, 7, 29, 0, 0), datetime(2022, 7, 31, 0, 0)),
        ])


if __name__ == '__main__':
    unittest.main()
