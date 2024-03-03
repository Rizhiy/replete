from __future__ import annotations

import datetime as dt
from typing import Iterable

from dateutil.relativedelta import relativedelta  # noqa: TCH002, required for doctests


def date_range(start: dt.date, stop: dt.date, step_days: int = 1) -> Iterable[dt.date]:
    """
    Simple `range`-like for `datetime.date`.

    >>> list(date_range(dt.date(2019, 12, 29), dt.date(2020, 1, 3), 2))
    [datetime.date(2019, 12, 29), datetime.date(2019, 12, 31), datetime.date(2020, 1, 2)]
    >>> list(date_range(dt.date(2020, 1, 3), dt.date(2019, 12, 29), -2))
    [datetime.date(2020, 1, 3), datetime.date(2020, 1, 1), datetime.date(2019, 12, 30)]
    >>> list(date_range(dt.date(2020, 1, 3), dt.date(2019, 12, 29), 1))
    []
    >>> list(date_range(dt.date(2019, 12, 29), dt.date(2020, 1, 3), -1))
    []
    """
    total_days = (stop - start).days
    for step in range(0, total_days, step_days):
        yield start + dt.timedelta(days=step)


def datetime_range(start: dt.datetime, stop: dt.datetime | None, step: dt.timedelta) -> Iterable[dt.datetime]:
    """
    :param stop: can be `None` to make an infinite generator.
    :param precise: use (slower) multiplication to avoid rounding errors.

    >>> def _dts_s(dts):
    ...     return [val.isoformat() for val in dts]
    ...
    >>> dt1 = dt.datetime(2022, 2, 2)
    >>> dt2 = dt.datetime(2022, 2, 4)
    >>> _dts_s(datetime_range(dt1, dt2, dt.timedelta(days=1)))
    ['2022-02-02T00:00:00', '2022-02-03T00:00:00']
    >>> _dts_s(datetime_range(dt1, dt2, dt.timedelta(hours=17)))
    ['2022-02-02T00:00:00', '2022-02-02T17:00:00', '2022-02-03T10:00:00']
    >>> _dts_s(datetime_range(dt1, dt2, dt.timedelta(seconds=11.11111111111)))[-1]
    '2022-02-03T23:59:59.998272'
    """
    if not step:
        raise ValueError(f"Step must be positive, step = {step}")
    forward = step > dt.timedelta()
    current = start
    while True:
        if stop is not None and ((current >= stop) if forward else (current <= stop)):
            return
        yield current
        current += step


def round_dt(
    datetime: dt.datetime,
    delta: dt.timedelta | relativedelta,
    start_time: dt.time = dt.time.min,
) -> dt.datetime:
    """
    Round time-from-midnight to the specified timedelta.

    Similar to postgresql's `date_trunc`, and `pandas.Timestamp.floor`.

    Only allows splitting the next larger scale evenly
    (e.g. 15-second interval evenly divides 60 seconds, but 40-second interval doesn't).

    >>> ts = dt.datetime(2021, 5, 3, 10, 37, 17)
    >>> round_dt(ts, dt.timedelta(seconds=10))
    datetime.datetime(2021, 5, 3, 10, 37, 10)
    >>> round_dt(ts, dt.timedelta(minutes=1))
    datetime.datetime(2021, 5, 3, 10, 37)
    >>> round_dt(ts, dt.timedelta(minutes=3))
    datetime.datetime(2021, 5, 3, 10, 36)
    >>> round_dt(ts, dt.timedelta(hours=2))
    datetime.datetime(2021, 5, 3, 10, 0)
    >>> round_dt(ts, dt.timedelta(days=1))
    datetime.datetime(2021, 5, 3, 0, 0)
    >>> round_dt(ts, relativedelta(months=1))
    datetime.datetime(2021, 5, 1, 0, 0)
    >>> round_dt(ts, relativedelta(years=1))
    datetime.datetime(2021, 1, 1, 0, 0)
    >>> round_dt(ts, dt.timedelta(seconds=1.234))
    Traceback (most recent call last):
    ...
    ValueError: Timedelta does not divide 60 seconds equally: 0:00:01.234000
    >>> round_dt(ts, dt.timedelta(days=400))
    Traceback (most recent call last):
    ...
    ValueError: Timedelta should be one day or less, got: 400 days, 0:00:00
    """
    if isinstance(delta, dt.timedelta):
        seconds = delta.total_seconds()
        scales = [60, 60 * 60, 60 * 60 * 24]  # minute, hour, day
        scale = next((scale for scale in scales if seconds <= scale), None)
        if scale:
            if scale % seconds != 0:
                raise ValueError(f"Timedelta does not divide {scale} seconds equally: {delta}")
            ts_start = datetime.replace(
                hour=start_time.hour,
                minute=start_time.minute,
                second=start_time.second,
                microsecond=start_time.microsecond,
            )
            return ts_start + dt.timedelta(seconds=(datetime - ts_start).total_seconds() // seconds * seconds)
        raise ValueError(f"Timedelta should be one day or less, got: {delta}")

    if any([delta.microseconds, delta.seconds, delta.minutes, delta.hours]):
        raise ValueError("relativedelta more precise than day is not supported, use timedelta")
    if not (delta.years or delta.months):
        raise ValueError("relativedelta should have at least one of years or months")

    datetime = datetime.replace(
        day=1,
        hour=start_time.hour,
        minute=start_time.minute,
        second=start_time.second,
        microsecond=start_time.microsecond,
    )

    if delta.years == 0:
        if delta.months not in [1, 2, 3, 4, 6]:
            raise ValueError(f"delta.months should be 1, 2, 3, 4 or 6. Got {delta=}")
        return datetime.replace(month=1 + (datetime.month - 1) // delta.months * delta.months)

    if delta.months != 0:
        raise ValueError(f"delta.months should be 0 if years are used. Got {delta=}")
    datetime = datetime.replace(month=1)
    return datetime.replace(year=datetime.year // delta.years * delta.years)
