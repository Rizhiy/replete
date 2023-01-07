# type: ignore
from __future__ import annotations

from typing import Type

import pytest

from nt_utils.register import Register


@pytest.fixture()
def base_class():
    class BaseClass(Register, base=True, abstract=True):
        pass

    return BaseClass


def test_registered_names(base_class: Type[Register]) -> None:
    class SubClass(base_class):
        pass

    assert set(base_class.get_registered_names()) == {"Sub"}


def test_get_subclass(base_class: Type[Register]) -> None:
    class SubClass(base_class):
        pass

    assert base_class.get_subclass("Sub") == SubClass


def test_get_all_subclasses(base_class: Type[Register]) -> None:
    class SubClass(base_class):
        pass

    assert set(base_class.get_all_subclases()) == {SubClass}


def test_get_name_in_register(base_class: Type[Register]) -> None:
    class SubClass(base_class):
        pass

    assert SubClass.get_name_in_register() == "Sub"
