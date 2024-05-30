from __future__ import annotations

import copy
import enum
import fcntl
from typing import TYPE_CHECKING, Self

if TYPE_CHECKING:
    from io import TextIOWrapper
    from pathlib import Path


class FileLockType(enum.Enum):
    EXCLUSIVE = enum.auto()
    SHARED = enum.auto()


# TODO: Make this re-entrant
class FileLock:
    LOCK_TYPE_TO_FCNTL_LOCK = {FileLockType.EXCLUSIVE: fcntl.LOCK_EX, FileLockType.SHARED: fcntl.LOCK_SH}

    def __init__(self, file_path: Path):
        self._file_path = file_path.with_suffix(".lock")
        self._file_path.parent.mkdir(parents=True, exist_ok=True)
        self._file_path.touch(exist_ok=True)

        self._fd: TextIOWrapper | None = None
        self._lock_code: int | None = None

    @property
    def file_path(self) -> Path:
        return self._file_path

    @property
    def read_lock(self) -> Self:
        if self._fd is not None:
            raise ValueError("Can't get read lock when lock is already acquired")
        self_copy = copy.copy(self)
        self_copy._lock_code = self.LOCK_TYPE_TO_FCNTL_LOCK[FileLockType.SHARED]  # noqa: SLF001
        return self_copy

    @property
    def write_lock(self) -> Self:
        if self._fd is not None:
            raise ValueError("Can't get read lock when lock is already acquired")
        self_copy = copy.copy(self)
        self_copy._lock_code = self.LOCK_TYPE_TO_FCNTL_LOCK[FileLockType.EXCLUSIVE]  # noqa: SLF001
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

    def __enter__(self) -> Self:
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
