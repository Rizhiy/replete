from __future__ import annotations

import hashlib
import json
import operator
from collections.abc import Mapping
from time import monotonic
from typing import Any, Dict, Sequence

import pytest
import xxhash
from nt_utils.consistent_hash import consistent_hash
from nt_utils.utils import grouped

CONSISTENT_HASH_TEST_CASES = [
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
]


@pytest.mark.parametrize("a,b,expected", CONSISTENT_HASH_TEST_CASES)
def test_consistent_hash(a, b, expected):
    result = consistent_hash(a) == consistent_hash(b)
    assert result == expected


def consistent_hash_ref(*args, **kwargs) -> int:
    """ Reference (old) implementation of `consistent_hash` """
    params = [*args, *sorted(kwargs.items(), key=operator.itemgetter(0))]
    hashes = []
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


def consistent_hash_ref2_raw(args: Sequence[Any] = (), kwargs: Dict[str, Any] = None) -> xxhash.xxh128:
    params = [*args, *sorted(kwargs.items())] if kwargs else args
    hasher = xxhash.xxh128()
    for param in params:
        if hasattr(param, "_consistent_hash"):
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


def consistent_hash_ref2(*args, **kwargs) -> int:
    return consistent_hash_ref2_raw(args, kwargs).intdigest()


def test_consistent_hash_ref_perf():
    def time_stuff(consistent_hash_func, count=1000, best_of=3) -> None:
        timings = []
        for _ in range(best_of):
            t01 = monotonic()
            for _ in range(count):
                for val1, val2, _ in CONSISTENT_HASH_TEST_CASES:
                    consistent_hash_func(val1)
                    consistent_hash_func(val2)
                consistent_hash_func(CONSISTENT_HASH_TEST_CASES)
            t02 = monotonic()
            timings.append(t02 - t01)
        return min(timings)

    for _ in range(2):  # hack to avoid possible cold-start effects
        actual_time = time_stuff(consistent_hash)
        ref2_time = time_stuff(consistent_hash_ref2)
        ref_time = time_stuff(consistent_hash_ref)

    print(dict(actual_time=actual_time, ref_time=ref_time, ref2_time=ref2_time))
    assert actual_time < ref_time
    # No significant difference expected for the current simple examples.
    assert actual_time < ref2_time * 1.3


def _sorted_any(values):
    return sorted(values, key=lambda val: json.dumps(val, sort_keys=True, default=repr))


def test_consistent_hash_ref_match():
    values = [CONSISTENT_HASH_TEST_CASES] + [
        val for val1, val2, _ in CONSISTENT_HASH_TEST_CASES for val in (val1, val2)
    ]
    groups = grouped((consistent_hash(val), val) for val in values)
    groups_ref = grouped((consistent_hash_ref(val), val) for val in values)
    assert _sorted_any(groups.values()) == _sorted_any(groups_ref.values())
