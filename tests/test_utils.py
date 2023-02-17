from __future__ import annotations

import random
import re
import time

import pytest

from nt_utils import Timer, ensure_unique_keys, split_list
from nt_utils.utils import futures_processing


def test_unique_keys():
    unique_keys = {"foo": "bar", "bar": "foo"}
    assert isinstance(ensure_unique_keys(unique_keys.items()), dict)

    non_unique_keys = [("foo", "bar"), ("foo", "foo")]
    with pytest.raises(ValueError, match="Key conflict"):
        ensure_unique_keys(non_unique_keys)


def test_split_list():
    integers = list(range(10))
    matching, non_matching = split_list(integers, lambda i: i < 5)
    assert set(matching) == set(integers[:5])
    assert set(non_matching) == set(integers[5:])


@pytest.fixture()
def futures_processing_test_vars():
    wait_time = 0.1

    def func(str_: str, *, num: int) -> str:
        time.sleep(wait_time + random.random() * 0.1)
        return str_ * num

    args = [(c,) for c in list("abcdefg")]
    kwargs = [{"num": i} for i in range(len(args))]

    return wait_time, func, args, kwargs


def test_futures_processing(futures_processing_test_vars):
    wait_time, func, args, kwargs = futures_processing_test_vars

    with Timer() as timer:
        result = set(futures_processing(func, args, kwargs))  # type: ignore
    simple_results = {func(*a, **kw) for a, kw in zip(args, kwargs)}  # type: ignore

    assert result == simple_results
    assert timer.time < wait_time * 2


def test_futures_processing_in_order(futures_processing_test_vars):
    wait_time, func, args, kwargs = futures_processing_test_vars

    with Timer() as timer:
        result = list(futures_processing(func, args, kwargs, in_order=True))  # type: ignore
    simple_results = [func(*a, **kw) for a, kw in zip(args, kwargs)]  # type: ignore

    assert result == simple_results
    assert timer.time < wait_time * 2


def test_futures_processing_with_exception():
    def func() -> None:
        raise ValueError("foo")

    with pytest.raises(ValueError, match="foo"):
        list(futures_processing(func, [()]))


def test_futures_processing_with_error_log(caplog):
    def func() -> None:
        raise ValueError("foo")

    list(futures_processing(func, [()], only_log_exceptions=True))
    assert re.search(r"Exception in processing .* with args .* and kwargs", caplog.text) is not None
    assert re.search(r"ValueError: foo", caplog.text) is not None
