from __future__ import annotations

import typing
from abc import abstractmethod
from typing import Any, Protocol

C = typing.TypeVar("C", bound="Comparable")


class Comparable(Protocol):
    """
    For details, see
    https://github.com/python/typing/issues/59#issuecomment-353878355
    """

    @abstractmethod
    def __eq__(self, other: Any) -> bool:
        pass

    @abstractmethod
    def __lt__(self: C, other: C) -> bool:
        pass
