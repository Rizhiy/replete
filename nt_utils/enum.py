from __future__ import annotations

from enum import Enum
from typing import Any


class ComparableEnum(Enum):
    def __eq__(self, other: Any) -> bool:
        return other.__class__ is self.__class__ and other.value == self.value

    def __lt__(self, other: Any) -> bool:
        if other.__class__ is not self.__class__:
            raise NotImplementedError
        return self.value < other.value

    def __hash__(self) -> int:
        return super().__hash__() ^ hash(self.__class__)
