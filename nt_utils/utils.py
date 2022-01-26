from __future__ import annotations

import datetime as dt
from typing import Dict, Hashable, Iterable, List, Sequence, Tuple, TypeVar

TKey = TypeVar("TKey", bound=Hashable)
TVal = TypeVar("TVal")


def grouped(items: Iterable[Tuple[TKey, TVal]]) -> Dict[TKey, List[TVal]]:
    """
    Similar to `itertools.groupby`, but returns a dict, accepts unsorted
    iterable, and works on pairs instead of `key=...`.

    >>> grouped([(1, 2), (3, 4), (1, 5)])
    {1: [2, 5], 3: [4]}
    """
    result = {}
    for key, value in items:
        lst = result.get(key)
        if lst is None:
            lst = []
            result[key] = lst
        lst.append(value)
    return result


TChunkValue = TypeVar("TChunkValue")


def chunks(seq: Sequence[TChunkValue], size: int) -> Iterable[Sequence[TChunkValue]]:
    """
    Iterate over slices of `seq` with at most `size` elements in each.

    >>> list(chunks(list(range(10)), 3))
    [[0, 1, 2], [3, 4, 5], [6, 7, 8], [9]]
    """
    for pos in range(0, len(seq), size):
        yield seq[pos : pos + size]


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


def ensure_unique_keys(items: Iterable[tuple[TKey, TVal]]) -> dict[TKey, TVal]:
    """ Replacement for dict comprehension that checks the keys uniqueness """
    result = {}
    for key, value in items:
        if key in result:
            raise ValueError(f"Key conflict: {key=!r}, first_value={result[key]!r}, second_value={value!r}")
        result[key] = value
    return result
