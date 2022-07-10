from __future__ import annotations

import logging
import sys
import traceback
import warnings
from collections import defaultdict

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


class change_root_level:
    def __init__(self, level: int, skip_handlers=False):
        self._level = level
        self._skip_handlers = skip_handlers
        self._original_level = None
        self._original_handler_levels = None

    def _update_levels(self, root_level: int, handler_levels=None):
        root_logger = logging.getLogger()
        root_logger.setLevel(root_level)
        if self._skip_handlers:
            return
        handler_levels = handler_levels or self._original_handler_levels or defaultdict(lambda: root_level)
        for handler in root_logger.handlers:
            handler.setLevel(handler_levels[handler])

    def __enter__(self) -> None:
        root_logger = logging.getLogger()
        self._original_level = root_logger.level
        self._original_handler_levels = {handler: handler.level for handler in root_logger.handlers}
        self._update_levels(self._level)

    def __exit__(self, *_):
        self._update_levels(self._original_level, self._original_handler_levels)
