""" Assorted utilities with minimal dependencies """
from __future__ import annotations

from .cli import autocli
from .consistent_hash import consistent_hash, picklehash
from .logging import warn_with_traceback
from .timer import Timer
from .utils import chunks, date_range, datetime_range, deep_update, ensure_unique_keys, grouped, split_list

__version__ = "1.9.1"
