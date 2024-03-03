from __future__ import annotations

import logging
from typing import Any, ClassVar, Iterable

LOGGER = logging.getLogger(__name__)


class RegisterError(Exception):
    """Common base class for `Register`-specific errors"""


class Register:
    """Keep track of all subclasses"""

    # Filled in `__init_subclass__`
    _name_in_register: ClassVar[str]
    _register_base_class: ClassVar[type[Register]]
    _register_data: ClassVar[dict[str, type[Register]]]
    _register_suffix: ClassVar[str]

    @classmethod
    def _set_register_base_class(cls, obj: type[Register], suffix: str = None) -> None:
        if hasattr(cls, "_register_base_class"):
            raise RegisterError(
                f"Can't set {obj} as base class, base class is already set to {cls._register_base_class}",
            )
        obj._register_base_class = obj  # noqa: SLF001
        obj._register_data = {}  # noqa: SLF001
        if suffix is None:
            suffix = obj.__name__
            if suffix.startswith("Base") and len(suffix) != 4:
                suffix = suffix[4:]
            if not suffix:
                raise ValueError(f"Can't find suffix from name = {obj.__name__}, please provide manually")
        obj._register_suffix = suffix  # noqa: SLF001 # type: ignore

    @classmethod
    def register_class(cls, obj: type, name: str = None) -> None:
        if not hasattr(cls, "_register_base_class"):
            raise AttributeError(f"Base class is not set for {cls}")
        if not issubclass(obj, cls._register_base_class):
            raise RegisterError(f"Can't register {obj} to {cls} as it is not a subclass!")

        if name is None:
            name = obj.__name__
            if name[-len(cls._register_suffix) :] == cls._register_suffix:
                name = name[: -len(cls._register_suffix)]

        old_cls = cls._register_data.get(name)
        if old_cls is not None:
            # Using `__dict__` instead of `hasattr` because `hasattr` includes superclasses.
            if "__attrs_attrs__" in cls.__dict__ and "__attrs_attrs__" not in old_cls.__dict__:
                old_cls._name_in_register = None  # noqa: SLF001 # type: ignore
            else:
                raise KeyError(f"{name} is already registered! (Most likely subclass name clash)")
        cls._register_data[name] = obj

        obj._name_in_register = name  # noqa: SLF001
        # Have to do this, since registered class might not be a subclass of Register.
        # "Cannot assign to a method", "expression has type "classmethod[Any]", variable has type "Callable[[], str]""
        obj.get_name_in_register = classmethod(Register.get_name_in_register.__func__)  # type: ignore

    def __init_subclass__(
        cls,
        *,
        base: bool = False,
        base_class: type = None,
        abstract: bool = False,
        suffix: str = None,
        name: str = None,
        **kwargs: Any,
    ) -> None:
        if suffix and not (base or base_class):
            raise RegisterError("Register suffix is only applicable for base class registration")
        if abstract and name is not None:
            raise RegisterError(f"Tried to register abstract class {cls} with name {name}")
        if base:
            cls._set_register_base_class(cls, suffix)
        if base_class is not None:
            cls._set_register_base_class(base_class, suffix)

        if not abstract:
            cls.register_class(cls, name=name)

        super().__init_subclass__(**kwargs)

    @classmethod
    def get_registered_names(cls) -> Iterable[str]:
        return cls._register_data.keys()

    @classmethod
    def get_subclass(cls, name: str) -> type:
        return cls._register_data[name]

    @classmethod
    def get_all_subclases(cls) -> Iterable[type]:
        return cls._register_data.values()

    @classmethod
    def get_name_in_register(cls) -> str:
        return cls._name_in_register


__all__ = ["RegisterError", "Register"]
