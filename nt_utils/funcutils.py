from __future__ import annotations

import operator
from typing import Callable, Iterable, TypeVar, Union, cast


class Marker:
    """Special class for comparison markers (for use instead of `NoneType`)"""


TLeft = TypeVar("TLeft")
TRight = TypeVar("TRight")
TRightDefault = TypeVar("TRightDefault")


def join_ffill(
    left_lst: Iterable[TLeft],
    right_lst: Iterable[TRight],
    condition: Callable[[TLeft, TRight], bool] = operator.ge,
    default: TRightDefault = None,
) -> Iterable[tuple[TLeft, Union[TRight, TRightDefault]]]:
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
    right_item: Union[TRight, TRightDefault] = cast(TRightDefault, default)
    next_right_item: Union[TRight, Marker] = next(right_iter, right_done_marker)
    for left_item in left_lst:
        if next_right_item is not right_done_marker and condition(left_item, cast(TRight, next_right_item)):
            right_item = cast(TRight, next_right_item)
            next_right_item = next(right_iter, right_done_marker)
        yield left_item, right_item


def join_backfill(
    left_lst: Iterable[TLeft],
    right_lst: Iterable[TRight],
    condition: Callable[[TLeft, TRight], bool] = operator.le,
    default: TRightDefault = None,
) -> Iterable[tuple[TLeft, Union[TRight, TRightDefault]]]:
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
    right_item = next(right_iter, right_done_marker)
    for left_item in left_lst:
        while right_item is not right_done_marker and not condition(left_item, cast(TRight, right_item)):
            right_item = next(right_iter, right_done_marker)
        yield left_item, cast(TRightDefault, default) if right_item is right_done_marker else cast(TRight, right_item)
