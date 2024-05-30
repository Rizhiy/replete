from __future__ import annotations

import copy
import fcntl
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from io import TextIOWrapper
    from pathlib import Path


# TODO: Make this re-entrant
class FileLock:
    """
    :param timeout: timeout in seconds
    """

    def __init__(self, file_path: Path):
        self._file_path = file_path.with_suffix(".lock")
        self._file_path.parent.mkdir(parents=True, exist_ok=True)
        self._file_path.touch(exist_ok=True)

        self._fd: TextIOWrapper | None = None
        self._lock_code: int | None = None

    @property
    def file_path(self) -> Path:
        return self._file_path

    def read_lock(self, *, non_blocking=False) -> FileLock:
        if self._fd is not None:
            raise ValueError("Can't get read lock when lock is already acquired")
        self_copy = copy.copy(self)
        self_copy._lock_code = fcntl.LOCK_SH  # noqa: SLF001
        if non_blocking:
            self_copy._lock_code |= fcntl.LOCK_NB  # noqa: SLF001
        return self_copy

    def write_lock(self, *, non_blocking=False) -> FileLock:
        if self._fd is not None:
            raise ValueError("Can't get read lock when lock is already acquired")
        self_copy = copy.copy(self)
        self_copy._lock_code = fcntl.LOCK_EX  # noqa: SLF001
        if non_blocking:
            self_copy._lock_code |= fcntl.LOCK_NB  # noqa: SLF001
        return self_copy

    def acquire(self) -> None:
        if self._lock_code is None:
            raise ValueError("Can't acquire bare lock, please use either read_lock or write_lock")
        self._fd = self._file_path.open()
        fcntl_lock = self._lock_code

        fcntl.flock(self._fd, fcntl_lock)

    def release(self) -> None:
        if not self._fd:
            raise ValueError(f"Lock on {self._file_path} is not acquired and cannot be released")
        fcntl.flock(self._fd, fcntl.LOCK_UN)
        self._fd.close()
        self._fd = None

    def __enter__(self) -> FileLock:
        self.acquire()
        return self

    def __exit__(self, *_) -> None:
        self.release()

    def __eq__(self, other):
        return all(
            getattr(self, attr_name) == getattr(other, attr_name) for attr_name in ["_file_path", "_lock_type", "_fd"]
        )

    def __reduce__(self):
        if self._fd is not None:
            raise ValueError("Can't pickle lock when it's acquired, release lock before pickling")
        return self.__class__, (self._file_path,)
