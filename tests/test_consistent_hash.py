from __future__ import annotations

import hashlib
import json
import operator
from collections.abc import Mapping
from typing import TYPE_CHECKING

import pytest
import xxhash

from replete import Timer, consistent_hash, grouped, picklehash

if TYPE_CHECKING:
    from collections.abc import Callable, Iterable, Sequence
    from typing import Any


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
    ({"cls": ConsistentHashObj}, {"cls": ConsistentHashObj}, True),
]


@pytest.mark.parametrize(("value_a", "value_b", "expected"), CONSISTENT_HASH_TEST_CASES)
def test_consistent_hash(value_a: Any, value_b: Any, expected: bool) -> None:
    result = consistent_hash(value_a) == consistent_hash(value_b)
    assert result == expected


def consistent_hash_ref(*args: Any, **kwargs: Any) -> int:
    """Reference (old) implementation of `consistent_hash`"""
    params = [*args, *sorted(kwargs.items(), key=operator.itemgetter(0))]
    hashes: list[int | str] = []
    for param in params:
        if isinstance(param, Mapping):
            hashes.append(consistent_hash(**{str(key): value for key, value in param.items()}))
        elif isinstance(param, (list, tuple)):
            hashes.append(consistent_hash(*param))
        else:
            hashes.append(repr(param))
    hasher = hashlib.md5()  # noqa: S324
    for hash_piece in hashes:
        hasher.update(str(hash_piece).encode())
    return int(hasher.hexdigest(), 16)


def consistent_hash_ref2_raw(args: Sequence[Any] = (), kwargs: dict[str, Any] | None = None) -> xxhash.xxh128:
    params = [*args, *sorted(kwargs.items())] if kwargs else args
    hasher = xxhash.xxh128()
    for param in params:
        if hasattr(param, "consistent_hash") and hasattr(param.consistent_hash, "__self__"):
            rec_int = param.consistent_hash()
            hasher.update(rec_int.to_bytes(16, "little"))
        elif isinstance(param, Mapping):
            rec = consistent_hash_ref2_raw((), {str(key): value for key, value in param.items()})
            hasher.update(rec.digest())
        elif isinstance(param, (list, tuple)):
            rec = consistent_hash_ref2_raw(param)
            hasher.update(rec.digest())
        else:
            hasher.update(repr(param).encode())
    return hasher


def consistent_hash_ref2(*args: Any, **kwargs: Any) -> int:
    return consistent_hash_ref2_raw(args, kwargs).intdigest()


def test_consistent_hash_ref_perf() -> None:
    def time_stuff(consistent_hash_func: Callable[..., Any], count: int = 1000) -> float:
        with Timer() as t:
            for _ in range(count):
                for val1, val2, _ in CONSISTENT_HASH_TEST_CASES:
                    consistent_hash_func(val1)
                    consistent_hash_func(val2)
                consistent_hash_func(CONSISTENT_HASH_TEST_CASES)
        return t.time

    funcs: list[Callable[..., Any]] = [consistent_hash, consistent_hash_ref2, consistent_hash_ref, picklehash]
    all_timings = [{func: time_stuff(func) for func in funcs} for _ in range(5)]
    min_timings = {key: min(timing[key] for timing in all_timings) for key in all_timings[0]}

    assert min_timings[consistent_hash] < min_timings[consistent_hash_ref]
    # No significant difference expected for the current simple examples.
    assert min_timings[consistent_hash] < min_timings[consistent_hash_ref2] * 1.5
    assert min_timings[picklehash] < min_timings[consistent_hash_ref2] * 0.8


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
    ph_groups = grouped((picklehash(val), val) for val in values)
    assert _sorted_any(ph_groups.values()) == _sorted_any(groups_ref.values())
