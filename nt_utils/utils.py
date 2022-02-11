from __future__ import annotations

import datetime as dt
from collections.abc import Callable, Hashable, Iterable, Mapping, Sequence
from typing import TypeVar, cast

TKey = TypeVar("TKey", bound=Hashable)
TVal = TypeVar("TVal")
# For `sort`-like `key=...` argument:
TSourceVal = TypeVar("TSourceVal")
TSortKey = Callable[[TSourceVal], TVal]


def grouped(items: Iterable[tuple[TKey, TVal]]) -> dict[TKey, list[TVal]]:
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
    """Replacement for dict comprehension that checks the keys uniqueness"""
    result = {}
    for key, value in items:
        if key in result:
            raise ValueError(f"Key conflict: {key=!r}, first_value={result[key]!r}, second_value={value!r}")
        result[key] = value
    return result


def deep_update(target: dict, updates: Mapping) -> dict:
    """
    >>> target = dict(a=1, b=dict(c=2, d=dict(e="f", g="h"), i=dict(j="k")))
    >>> updates = dict(i="i", j="j", b=dict(c=dict(c2="c2"), d=dict(e="f2")))
    >>> deep_update(target, updates)
    {'a': 1, 'b': {'c': {'c2': 'c2'}, 'd': {'e': 'f2', 'g': 'h'}, 'i': {'j': 'k'}}, 'i': 'i', 'j': 'j'}
    """
    target = target.copy()
    for key, value in updates.items():
        old_value = target.get(key)
        if isinstance(old_value, dict):
            new_value = deep_update(old_value, value)
        else:
            new_value = value
        target[key] = new_value
    return target


def bisect_left(
    data: Sequence[TSourceVal],
    value: TVal,
    lo: int = 0,
    hi: int = None,
    key: TSortKey = cast(TSortKey, lambda val: val),
):
    """
    `bisect.bisect_left` with the additional `key` support.

    >>> data = [dict(val=val) for val in [2, 4, 8, 8, 10, 12]]
    >>> values = list(range(14))
    >>> [bisect_left(data, val, key=lambda item: item["val"]) for val in values]
    [0, 0, 0, 1, 1, 2, 2, 2, 2, 4, 4, 5, 5, 6]
    """
    assert lo >= 0
    left = lo
    right = len(data) if hi is None else hi
    while left < right:
        middle = (left + right) // 2
        if key(data[middle]) < value:
            left = middle + 1
        else:
            right = middle
    return left


def bisect_right(
    data: Sequence[TSourceVal],
    value: TVal,
    lo: int = 0,
    hi: int = None,
    key: TSortKey = cast(TSortKey, lambda val: val),
):
    """
    `bisect.bisect_right` with the additional `key` support.

    >>> data = [dict(val=val) for val in [2, 4, 8, 8, 10, 12]]
    >>> values = list(range(14))
    >>> [bisect_right(data, val, key=lambda item: item["val"]) for val in values]
    [0, 0, 1, 1, 2, 2, 2, 2, 4, 4, 5, 5, 6, 6]
    """
    assert lo >= 0
    left = lo
    right = len(data) if hi is None else hi
    while left < right:
        middle = (left + right) // 2
        if value < key(data[middle]):
            right = middle
        else:
            left = middle + 1
    return left
