""" Assorted utilities with minimal dependencies """
from __future__ import annotations

from .cli import autocli
from .consistent_hash import consistent_hash, picklehash
from .datetime import date_range, datetime_range, round_dt
from .logging import warn_with_traceback
from .timer import Timer
from .utils import chunks, deep_update, ensure_unique_keys, grouped, split_list

__version__ = "1.9.1"
