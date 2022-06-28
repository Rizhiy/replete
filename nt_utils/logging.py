from __future__ import annotations

import sys
import traceback
import warnings

ORIGINAL_SHOWWARNINGS = warnings.showwarning


def _warn_with_traceback(message, category, filename, lineno, file=None, line=None):
    log = file if hasattr(file, "write") else sys.stderr
    traceback.print_stack(file=log)
    ORIGINAL_SHOWWARNINGS(message, category, filename, lineno, file, line)


class warn_with_traceback:
    def __enter__(self):
        self._orig_show = warnings.showwarning
        warnings.showwarning = _warn_with_traceback

    def __exit__(self, *_):
        warnings.showwarning = ORIGINAL_SHOWWARNINGS
