from __future__ import annotations

import pytest

from nt_utils import ensure_unique_keys, split_list


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
