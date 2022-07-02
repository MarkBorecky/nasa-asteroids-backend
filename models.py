from dataclasses import dataclass
from datetime import date
from pydantic import BaseModel
from dateutil.rrule import rrule, DAILY


@dataclass(frozen=True)
class Asteroid:
    id: str
    name: str
    date: date
    miss_distance_in_kilometers: float


@dataclass(frozen=True)
class DateRange(BaseModel):
    start: date
    end: date

    def days(self):
        return [dt for dt in rrule(DAILY, dtstart=self.start, until=self.end)]

    def is_empty(self) -> bool:
        return False


class EmptyDateRange(DateRange):
    def __init__(self):
        super().__init__(None, None)

    def is_empty(self) -> bool:
        return True


class DateRangeCollector:
    def __init__(self):
        self.ranges: [DateRange] = []
        self.current: DateRange = EmptyDateRange()

    def add(self, next_date: date):
        if self.current.is_empty():
            self.current = DateRange(next_date, next_date)
        elif self.is_next_day(next_date) and self.start_diff(next_date) <= 6:
            self.current = DateRange(self.current.start, next_date)
        else:
            self.ranges.append(self.current)
            self.current = DateRange(next_date, next_date)

    def start_diff(self, next_date: date):
        return (next_date - self.current.start).days

    def is_next_day(self, next_date: date) -> bool:
        return (next_date - self.current.end).days == 1

    def days_from_start(self, next_date):
        return (next_date - self.current.start).days

    def finish(self) -> [DateRange]:
        self.ranges.append(self.current)
        return self.ranges


@dataclass(frozen=True)
class AsteroidToFetch:
    date: date
