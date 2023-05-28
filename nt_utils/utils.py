from __future__ import annotations

import functools
import itertools
import logging
import weakref
from concurrent import futures
from typing import TYPE_CHECKING, Any, Callable, Hashable, Iterable, Iterator, Mapping, Sequence, TypeVar, cast

from nt_utils.abc import Comparable

LOGGER = logging.getLogger(__name__)

if TYPE_CHECKING:
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


def split_list(items: Iterable[TVal], condition: Callable[[TVal], bool]) -> tuple[list[TVal], list[TVal]]:
    """
    Split list items into `(matching, non_matching)` by `cond(item)` callable.
    """
    matching = []
    non_matching = []
    for item in items:
        if condition(item):
            matching.append(item)
        else:
            non_matching.append(item)
    return matching, non_matching


def ensure_unique_keys(items: Iterable[tuple[TKey, TVal]]) -> dict[TKey, TVal]:
    """Replacement for dict comprehension that checks the keys uniqueness"""
    result: dict[TKey, TVal] = {}
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


def futures_processing(
    func: Callable,
    args_list: list[tuple] = None,
    kwargs_list: list[dict] = None,
    max_workers: int = None,
    in_order=False,
    only_log_exceptions=False,
) -> Iterator:
    """Process data concurrently"""
    if args_list is None and kwargs_list is None:
        raise ValueError("Must provide either args_list or kwargs_list")
    if args_list is None:
        args_list = [()] * len(kwargs_list)
    if kwargs_list is None:
        kwargs_list = [{}] * len(args_list)
    assert len(args_list) == len(kwargs_list), "args_list and kwargs_list must be the same length"

    def func_with_idx(idx, *args, **kwargs) -> tuple[int, Any]:
        try:
            return idx, func(*args, **kwargs)
        except Exception:
            LOGGER.exception(f"Exception in processing {func} with args {args} and kwargs {kwargs}")
            if only_log_exceptions:
                return idx, None
            raise

    with futures.ThreadPoolExecutor(max_workers=max_workers) as executor:
        idx_args_gen = enumerate(zip(args_list, kwargs_list))
        results = [executor.submit(func_with_idx, idx, *args, **kwargs) for idx, (args, kwargs) in idx_args_gen]

        cache_results = {}
        current_result_idx = 0
        for future in futures.as_completed(results):
            if future.exception():
                raise future.exception()
            idx, func_result = future.result()
            if in_order:
                cache_results[idx] = func_result
                while current_result_idx in cache_results:
                    yield cache_results.pop(current_result_idx)
                    current_result_idx += 1
            else:
                yield func_result


def weak_lru_cache(maxsize=128, typed=False):
    """LRU Cache decorator that keeps a weak reference to 'self'"""

    def helper(maxsize: int, typed: bool, user_function: Callable) -> Callable:
        @functools.lru_cache(maxsize, typed)
        def _func(_self, *args, **kwargs):
            return user_function(_self(), *args, **kwargs)

        @functools.wraps(user_function)
        def inner(self, *args, **kwargs):
            return _func(weakref.ref(self), *args, **kwargs)

        return inner

    if callable(maxsize) and isinstance(typed, bool):
        # The user_function was passed in directly via the maxsize argument
        user_function, maxsize = maxsize, 128
        return helper(maxsize, typed, user_function)
    assert type(maxsize) == int or maxsize is None, "Expected maxsize to be an integer or None"

    return functools.partial(helper, maxsize, typed)
