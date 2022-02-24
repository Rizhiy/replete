from __future__ import annotations

import hashlib
import json
import operator
from collections.abc import Callable, Iterable, Mapping, Sequence
from time import process_time
from typing import Any, Optional, Union

import pytest
import xxhash

from nt_utils.consistent_hash import consistent_hash
from nt_utils.utils import grouped


class ConsistentHashObj:
    def __init__(self, value: int):
        self._value = value

    def _consistent_hash(self) -> int:
        return self._value

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}({self._value})"


CONSISTENT_HASH_TEST_CASES: list[tuple[Any, Any, bool]] = [
    # value, value, equal
    ({}, {}, True),
    ({"foo": 1, "bar": 2}, {"bar": 2, "foo": 1}, True),
    ((1,), [1], True),
    (1, 1, True),
    (1, 2, False),
    (-1, -2, False),
    ((1,), [2], False),
    ([1, 2], [2, 1], False),
    ({"foo": 1, "bar": 2}, {"foo": 1, "quux": 2}, False),
    (ConsistentHashObj(123), ConsistentHashObj(123), True),
    (ConsistentHashObj(123), ConsistentHashObj(1234), False),
    (dict(cls=ConsistentHashObj), dict(cls=ConsistentHashObj), True),
]


@pytest.mark.parametrize("a,b,expected", CONSISTENT_HASH_TEST_CASES)
def test_consistent_hash(a: Any, b: Any, expected: bool) -> None:
    result = consistent_hash(a) == consistent_hash(b)
    assert result == expected


def consistent_hash_ref(*args: Any, **kwargs: Any) -> int:
    """Reference (old) implementation of `consistent_hash`"""
    params = [*args, *sorted(kwargs.items(), key=operator.itemgetter(0))]
    hashes: list[Union[int, str]] = []
    for param in params:
        if isinstance(param, Mapping):
            hashes.append(consistent_hash(**{str(key): value for key, value in param.items()}))
        elif isinstance(param, (list, tuple)):
            hashes.append(consistent_hash(*param))
        else:
            hashes.append(repr(param))
    hasher = hashlib.md5()
    for h in hashes:
        hasher.update(str(h).encode())
    return int(hasher.hexdigest(), 16)


def consistent_hash_ref2_raw(args: Sequence[Any] = (), kwargs: Optional[dict[str, Any]] = None) -> xxhash.xxh128:
    params = [*args, *sorted(kwargs.items())] if kwargs else args
    hasher = xxhash.xxh128()
    for param in params:
        if hasattr(param, "_consistent_hash") and hasattr(param._consistent_hash, "__self__"):
            rec_int = param._consistent_hash()
            hasher.update(rec_int.to_bytes(16, "little"))
        elif isinstance(param, Mapping):
            rec = consistent_hash_ref2_raw((), {str(key): value for key, value in param.items()})
            hasher.update(rec.digest())
        elif isinstance(param, (list, tuple)):
            rec = consistent_hash_ref2_raw(param)
            hasher.update(rec.digest())
        else:
            hasher.update(repr(param).encode())  # TODO: use `pickle.dumps` instead.
    return hasher


def consistent_hash_ref2(*args: Any, **kwargs: Any) -> int:
    return consistent_hash_ref2_raw(args, kwargs).intdigest()


def test_consistent_hash_ref_perf() -> None:
    def time_stuff(consistent_hash_func: Callable[..., Any], count: int = 1000) -> float:
        t01 = process_time()
        for _ in range(count):
            for val1, val2, _ in CONSISTENT_HASH_TEST_CASES:
                consistent_hash_func(val1)
                consistent_hash_func(val2)
            consistent_hash_func(CONSISTENT_HASH_TEST_CASES)
        return process_time() - t01

    funcs = [consistent_hash, consistent_hash_ref2, consistent_hash_ref]
    all_timings = [{func: time_stuff(func) for func in funcs} for _ in range(5)]
    min_timings = {key: min(timing[key] for timing in all_timings) for key in all_timings[0]}

    assert min_timings[consistent_hash] < min_timings[consistent_hash_ref]
    # No significant difference expected for the current simple examples.
    assert min_timings[consistent_hash] < min_timings[consistent_hash_ref2] * 1.3


def _sorted_any(values: Iterable[Any]) -> list[Any]:
    return sorted(values, key=lambda val: json.dumps(val, sort_keys=True, default=repr))


def test_consistent_hash_ref_match() -> None:
    """Compare implementations on arbitrary supported values"""
    values = [
        *[val for val1, val2, _ in CONSISTENT_HASH_TEST_CASES for val in (val1, val2)],
        *CONSISTENT_HASH_TEST_CASES,
        CONSISTENT_HASH_TEST_CASES,
    ]
    groups = grouped((consistent_hash(val), val) for val in values)
    groups_ref = grouped((consistent_hash_ref(val), val) for val in values)
    assert _sorted_any(groups.values()) == _sorted_any(groups_ref.values())
