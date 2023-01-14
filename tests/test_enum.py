from __future__ import annotations

from enum import auto

import pytest

from nt_utils import ComparableEnum


class SomeEnum(ComparableEnum):
    One = auto()
    Two = auto()
    Three = auto()


class AnotherEnum(ComparableEnum):
    One = auto()
    Two = auto()
    Three = auto()


def test_eq():
    assert SomeEnum.One == SomeEnum.One
    assert SomeEnum.One != SomeEnum.Two
    assert SomeEnum.One != AnotherEnum.One


def test_lt():
    assert SomeEnum.One < SomeEnum.Two
    with pytest.raises(NotImplementedError):
        SomeEnum.One < AnotherEnum.One  # noqa: B015


def test_gt():
    assert SomeEnum.Two > SomeEnum.One


def test_sort():
    assert sorted([SomeEnum.Three, SomeEnum.One, SomeEnum.Two]) == [SomeEnum.One, SomeEnum.Two, SomeEnum.Three]
