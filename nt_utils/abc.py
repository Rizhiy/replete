from __future__ import annotations

import typing
from abc import abstractmethod
from typing import TYPE_CHECKING, Protocol

if TYPE_CHECKING:
    from typing import Any


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
