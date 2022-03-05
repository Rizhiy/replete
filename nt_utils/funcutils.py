from __future__ import annotations

import operator
from collections.abc import Callable, Iterable
from typing import Any, Generic, Optional, TypeVar, Union, cast, overload


class Marker:
    """Special class for comparison markers (for use instead of `NoneType`)"""


TLeft = TypeVar("TLeft")
TRight = TypeVar("TRight")
TRightDefault = TypeVar("TRightDefault")


@overload
def join_ffill(
    left_lst: Iterable[TLeft],
    right_lst: Iterable[TRight],
    condition: Callable[[TLeft, TRight], bool] = operator.ge,
    default: None = None,
) -> Iterable[tuple[TLeft, Union[TRight, None]]]:
    ...


@overload
def join_ffill(
    left_lst: Iterable[TLeft],
    right_lst: Iterable[TRight],
    condition: Callable[[TLeft, TRight], bool],
    default: TRightDefault,
) -> Iterable[tuple[TLeft, Union[TRight, TRightDefault]]]:
    ...


def join_ffill(
    left_lst: Iterable[TLeft],
    right_lst: Iterable[TRight],
    condition: Callable[[TLeft, TRight], bool] = operator.ge,
    default: Optional[TRightDefault] = None,
) -> Iterable[tuple[TLeft, Union[TRight, Optional[TRightDefault]]]]:
    """
    Join values to a sorted `left_lst` from sorted `right_lst`,
    switching to next `right_lst` item when `condition` passes
    (starting with `default`).

    Similar to `pandas.DataFrame.reindex(..., method="ffill")` + `pandas.DataFrame.join`.

    >>> right_side = [(2, 22), (4, 44), (7, 77)]
    >>> res = join_ffill(range(10), right_side, lambda v1, v2: v1 >= v2[0], default=(None, None))
    >>> from pprint import pprint
    >>> pprint(list(res))
    [(0, (None, None)),
     (1, (None, None)),
     (2, (2, 22)),
     (3, (2, 22)),
     (4, (4, 44)),
     (5, (4, 44)),
     (6, (4, 44)),
     (7, (7, 77)),
     (8, (7, 77)),
     (9, (7, 77))]
    >>> list(join_ffill(range(3), []))
    [(0, None), (1, None), (2, None)]
    >>> list(join_ffill(range(3), [1], default=0))
    [(0, 0), (1, 1), (2, 1)]
    """
    right_iter = iter(right_lst)
    right_done_marker = Marker()
    right_item: Union[TRight, Optional[TRightDefault]] = default
    next_right_item: Union[TRight, Marker] = next(right_iter, right_done_marker)
    for left_item in left_lst:
        while next_right_item is not right_done_marker and condition(left_item, cast(TRight, next_right_item)):
            right_item = cast(TRight, next_right_item)
            next_right_item = next(right_iter, right_done_marker)
        yield left_item, right_item


@overload
def join_backfill(
    left_lst: Iterable[TLeft],
    right_lst: Iterable[TRight],
    condition: Callable[[TLeft, TRight], bool] = operator.le,
    default: None = None,
) -> Iterable[tuple[TLeft, Union[TRight, None]]]:
    ...


@overload
def join_backfill(
    left_lst: Iterable[TLeft],
    right_lst: Iterable[TRight],
    condition: Callable[[TLeft, TRight], bool],
    default: TRightDefault,
) -> Iterable[tuple[TLeft, Union[TRight, TRightDefault]]]:
    ...


def join_backfill(
    left_lst: Iterable[TLeft],
    right_lst: Iterable[TRight],
    condition: Callable[[TLeft, TRight], bool] = operator.le,
    default: Optional[TRightDefault] = None,
) -> Iterable[tuple[TLeft, Union[TRight, Optional[TRightDefault]]]]:
    """
    Join values to a sorted `left_lst` from sorted `right_lst`,
    switching to next `right_lst` item (or `default`) when `condition` stops passing.

    Similar to `pandas.DataFrame.reindex(..., method="backfill")` + `pandas.DataFrame.join`.

    >>> right_side = [(2, 22), (4, 44), (4, 441), (7, 77)]
    >>> res = join_backfill(range(10), right_side, lambda v1, v2: v1 <= v2[0], default=(None, None))
    >>> from pprint import pprint
    >>> pprint(list(res))
    [(0, (2, 22)),
     (1, (2, 22)),
     (2, (2, 22)),
     (3, (4, 44)),
     (4, (4, 44)),
     (5, (7, 77)),
     (6, (7, 77)),
     (7, (7, 77)),
     (8, (None, None)),
     (9, (None, None))]
    >>> list(join_backfill(range(3), []))
    [(0, None), (1, None), (2, None)]
    >>> list(join_backfill(range(3), [1], default=0))
    [(0, 1), (1, 1), (2, 0)]
    """
    right_iter = iter(right_lst)
    right_done_marker = Marker()
    right_item: Union[TRight, Marker] = next(right_iter, right_done_marker)
    for left_item in left_lst:
        while right_item is not right_done_marker and not condition(left_item, cast(TRight, right_item)):
            right_item = next(right_iter, right_done_marker)
        yield left_item, default if right_item is right_done_marker else cast(TRight, right_item)


TObj = TypeVar("TObj")
TRes = TypeVar("TRes")


class cached_property(Generic[TObj, TRes]):
    """
    See
    https://github.com/django/django/blob/c6b4d62fa2c7f73b87f6ae7e8cf1d64ee5312dc5/django/utils/functional.py#L57
    """

    name: Optional[str] = None

    def __init__(self, func: Callable[[TObj], TRes]):
        self.func = func
        self.__doc__ = getattr(func, "__doc__")

    def __set_name__(self, owner: Any, name: str) -> None:
        if self.name is None:
            self.name = name
        elif name != self.name:
            raise TypeError(f"Cannot assign the same cached_property to two different names ({self.name} and {name}).")

    def __get__(self, instance: TObj, cls: Any = None) -> Union[TRes, cached_property[TObj, TRes]]:
        if instance is None:
            return self
        if self.name is None:
            raise TypeError("Cannot use cached_property instance without calling `__set_name__` on it.")
        res = self.func(instance)
        instance.__dict__[self.name] = res
        return res
