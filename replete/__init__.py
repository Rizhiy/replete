"""Assorted utilities with minimal dependencies"""

from __future__ import annotations

from .aio import LazyWrapAsync, achunked
from .cli import autocli
from .consistent_hash import consistent_hash, picklehash
from .datetime import date_range, datetime_range, round_dt
from .enum import ComparableEnum
from .logging import WarnWithTraceback, assert_with_logging, setup_logging
from .register import Register
from .timing import RateLimiter, Timer
from .utils import chunks, deep_update, ensure_unique_keys, grouped, split_list

__version__ = "2.0.1"
