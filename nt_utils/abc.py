from __future__ import annotations

import typing
from abc import abstractmethod
from typing import Any, Protocol

Cls = typing.TypeVar("Cls", bound="Comparable")


class Comparable(Protocol):
    """
    For details, see
    https://github.com/python/typing/issues/59#issuecomment-353878355
    """

    @abstractmethod
    def __eq__(self, other: Any) -> bool:
        pass

    @abstractmethod
    def __lt__(self: Cls, other: Cls) -> bool:
        pass
