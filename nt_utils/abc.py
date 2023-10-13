from __future__ import annotations

import typing
from abc import abstractmethod
from typing import TYPE_CHECKING, Protocol

if TYPE_CHECKING:
    from typing import Any


Cls = typing.TypeVar("Cls", bound="Comparable")


# https://github.com/python/typing/issues/59#issuecomment-353878355
class Comparable(Protocol):
    """Type annotation for comparable objects"""

    @abstractmethod
    def __eq__(self, other: Any) -> bool:
        """Compare two objects for equality"""

    @abstractmethod
    def __lt__(self: Cls, other: Cls) -> bool:
        """Compare two objects for less-than"""
