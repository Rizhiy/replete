from __future__ import annotations

import logging
import operator
from typing import TYPE_CHECKING, Callable, Iterable, Iterator, TypeVar, cast, overload

if TYPE_CHECKING:
    TRightDefault = TypeVar("TRightDefault")
TLeft = TypeVar("TLeft")
TRight = TypeVar("TRight")

LOGGER = logging.getLogger(__name__)


class Marker:
    """Special class for comparison markers (for use instead of `NoneType`)"""


@overload
def join_ffill(
    left_lst: Iterable[TLeft],
    right_lst: Iterable[TRight],
    condition: Callable[[TLeft, TRight], bool] = cast(Callable[[TLeft, TRight], bool], operator.ge),
    default: None = None,
) -> Iterable[tuple[TLeft, TRight | None]]: ...


@overload
def join_ffill(
    left_lst: Iterable[TLeft],
    right_lst: Iterable[TRight],
    condition: Callable[[TLeft, TRight], bool],
    default: TRightDefault,
) -> Iterable[tuple[TLeft, TRight | TRightDefault]]: ...


def join_ffill(
    left_lst: Iterable[TLeft],
    right_lst: Iterable[TRight],
    condition: Callable[[TLeft, TRight], bool] = cast(Callable[[TLeft, TRight], bool], operator.ge),
    default: TRightDefault | None = None,
) -> Iterable[tuple[TLeft, TRight | TRightDefault | None]]:
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
    right_item: TRight | TRightDefault | None = default
    next_right_item: TRight | Marker = next(right_iter, right_done_marker)
    for left_item in left_lst:
        while next_right_item is not right_done_marker and condition(left_item, cast(TRight, next_right_item)):
            right_item = cast(TRight, next_right_item)
            next_right_item = next(right_iter, right_done_marker)
        yield left_item, right_item


@overload
def join_backfill(
    left_lst: Iterable[TLeft],
    right_lst: Iterable[TRight],
    condition: Callable[[TLeft, TRight], bool] = cast(Callable[[TLeft, TRight], bool], operator.le),
    default: None = None,
) -> Iterable[tuple[TLeft, TRight | None]]: ...


@overload
def join_backfill(
    left_lst: Iterable[TLeft],
    right_lst: Iterable[TRight],
    condition: Callable[[TLeft, TRight], bool],
    default: TRightDefault,
) -> Iterable[tuple[TLeft, TRight | TRightDefault]]: ...


def join_backfill(
    left_lst: Iterable[TLeft],
    right_lst: Iterable[TRight],
    condition: Callable[[TLeft, TRight], bool] = cast(Callable[[TLeft, TRight], bool], operator.le),
    default: TRightDefault | None = None,
) -> Iterable[tuple[TLeft, TRight | TRightDefault | None]]:
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
    right_item: TRight | Marker = next(right_iter, right_done_marker)
    for left_item in left_lst:
        while right_item is not right_done_marker and not condition(left_item, cast(TRight, right_item)):
            right_item = next(right_iter, right_done_marker)
        yield left_item, default if right_item is right_done_marker else cast(TRight, right_item)


def yield_or_skip(iter_: Iterable, func: Callable, skip_on_errors: Iterable[type[Exception]]) -> Iterator:
    skip_on_errors = tuple(skip_on_errors)
    for item in iter_:
        try:
            yield func(item)
        except Exception as e:  # noqa: PERF203 intentional
            if isinstance(e, skip_on_errors):
                LOGGER.debug(f"Skipping {item} due to {e}")
                continue
            raise
