from __future__ import annotations

import datetime as dt
import itertools
from typing import TYPE_CHECKING, cast

if TYPE_CHECKING:
    from collections.abc import Callable, Hashable, Iterable, Iterator, Mapping, Sequence
    from typing import Any, TypeVar

    from nt_utils.abc import Comparable

    TKey = TypeVar("TKey", bound=Hashable)
    TVal = TypeVar("TVal")
    # For `sort`-like `key=...` argument:
    TSourceVal = TypeVar("TSourceVal")
    TCmpVal = TypeVar("TCmpVal", bound=Comparable)
    TSortKey = Callable[[TSourceVal], TCmpVal]


def grouped(items: Iterable[tuple[TKey, TVal]]) -> dict[TKey, list[TVal]]:
    """
    Similar to `itertools.groupby`, but returns a dict, accepts unsorted
    iterable, and works on pairs instead of `key=...`.

    >>> grouped([(1, 2), (3, 4), (1, 5)])
    {1: [2, 5], 3: [4]}
    """
    result: dict[TKey, list[TVal]] = {}
    for key, value in items:
        lst = result.get(key)
        if lst is None:
            lst = []
            result[key] = lst
        lst.append(value)
    return result


def chunks(seq: Sequence[TVal], size: int) -> Iterator[Sequence[TVal]]:
    """
    Iterate over slices of `seq` with at most `size` elements in each.

    >>> list(chunks(list(range(10)), 3))
    [[0, 1, 2], [3, 4, 5], [6, 7, 8], [9]]
    """
    for pos in range(0, len(seq), size):
        yield seq[pos : pos + size]


def iterchunks(iterable: Iterable[TVal], size: int) -> Iterator[Sequence[TVal]]:
    """
    Iterate over slices of `seq` with at most `size` elements in each.

    >>> list(iterchunks(range(10), 3))
    [(0, 1, 2), (3, 4, 5), (6, 7, 8), (9,)]
    """
    assert size > 0
    iterator = iter(iterable)
    while True:
        chunk = tuple(itertools.islice(iterator, size))
        if not chunk:
            return
        yield chunk


def window(iterable: Iterable[TVal], size: int, *, strict_size: bool = True) -> Iterator[Sequence[TVal]]:
    """
    >>> list(window(range(5), 3))
    [(0, 1, 2), (1, 2, 3), (2, 3, 4)]
    >>> list(window(range(3), 3))
    [(0, 1, 2)]
    >>> list(window(range(2), 3))
    []
    >>> list(window(range(2), 3, strict_size=False))
    [(0, 1)]
    """
    iterator = iter(iterable)
    result = tuple(itertools.islice(iterator, size))
    if strict_size and len(result) < size:
        return
    if len(result) <= size:
        yield result
    for elem in iterator:
        result = result[1:] + (elem,)
        yield result


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
    assert step, "must be non-zero"
    forward = step > dt.timedelta()
    current = start
    while True:
        if stop is not None and ((current >= stop) if forward else (current <= stop)):
            return
        yield current
        current += step


def ensure_unique_keys(items: Iterable[tuple[TKey, TVal]]) -> dict[TKey, TVal]:
    """Replacement for dict comprehension that checks the keys uniqueness"""
    result: dict[TKey, TVal] = {}
    for key, value in items:
        if key in result:
            raise ValueError(f"Key conflict: {key=!r}, first_value={result[key]!r}, second_value={value!r}")
        result[key] = value
    return result


def deep_update(target: dict[Any, Any], updates: Mapping[Any, Any]) -> dict[Any, Any]:
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
    value: TCmpVal,
    lo: int = 0,
    hi: int | None = None,
    key: TSortKey[TSourceVal, TCmpVal] | None = None,
) -> int:
    """
    `bisect.bisect_left` with the additional `key` support.

    >>> data = [dict(val=val) for val in [2, 4, 8, 8, 10, 12]]
    >>> values = list(range(14))
    >>> [bisect_left(data, val, key=lambda item: item["val"]) for val in values]
    [0, 0, 0, 1, 1, 2, 2, 2, 2, 4, 4, 5, 5, 6]
    """
    assert lo >= 0
    if key is None:
        key = lambda val: cast(TCmpVal, val)
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
    value: TCmpVal,
    lo: int = 0,
    hi: int | None = None,
    key: TSortKey[TSourceVal, TCmpVal] | None = None,
) -> int:
    """
    `bisect.bisect_right` with the additional `key` support.

    >>> data = [dict(val=val) for val in [2, 4, 8, 8, 10, 12]]
    >>> values = list(range(14))
    >>> [bisect_right(data, val, key=lambda item: item["val"]) for val in values]
    [0, 0, 1, 1, 2, 2, 2, 2, 4, 4, 5, 5, 6, 6]
    """
    assert lo >= 0
    if key is None:
        key = lambda val: cast(TCmpVal, val)
    left = lo
    right = len(data) if hi is None else hi
    while left < right:
        middle = (left + right) // 2
        if value < key(data[middle]):
            right = middle
        else:
            left = middle + 1
    return left
