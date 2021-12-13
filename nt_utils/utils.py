from __future__ import annotations

from typing import Dict, Hashable, Iterable, List, Tuple, TypeVar

TGroupedKey = TypeVar("TGroupedKey", bound=Hashable)
TGroupedVal = TypeVar("TGroupedVal")


def grouped(items: Iterable[Tuple[TGroupedKey, TGroupedVal]]) -> Dict[TGroupedKey, List[TGroupedVal]]:
    """
    Similar to `itertools.groupby`, but returns a dict, and works on pairs
    instead of `key=...`.

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
