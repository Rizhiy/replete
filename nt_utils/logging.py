from __future__ import annotations

import logging
import sys
import traceback
import warnings

ORIGINAL_SHOWWARNINGS = warnings.showwarning


def _warn_with_traceback(message, category, filename, lineno, file=None, line=None):
    log = file if hasattr(file, "write") else sys.stderr
    traceback.print_stack(file=log)
    ORIGINAL_SHOWWARNINGS(message, category, filename, lineno, file, line)


class warn_with_traceback:
    def __enter__(self) -> None:
        self._orig_show = warnings.showwarning
        warnings.showwarning = _warn_with_traceback

    def __exit__(self, *_):
        warnings.showwarning = ORIGINAL_SHOWWARNINGS


class change_logging_level:
    def __init__(self, level: int):
        self._level = level
        self._original_level: int = None

    def __enter__(self) -> None:
        root_logger = logging.getLogger()
        self._original_level = root_logger.level
        root_logger.setLevel(self._level)

    def __exit__(self, *_):
        logging.getLogger().setLevel(self._original_level)
        self._original_level = None
