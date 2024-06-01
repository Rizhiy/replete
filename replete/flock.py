from __future__ import annotations

import copy
import fcntl
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from io import TextIOWrapper
    from pathlib import Path


class FileLock:
    """
    :param timeout: timeout in seconds
    """

    def __init__(self, file_path: Path):
        self._file_path = file_path.with_suffix(".lock")
        self._file_path.parent.mkdir(parents=True, exist_ok=True)
        self._file_path.touch(exist_ok=True)

        self._locked = False
        self._fd: TextIOWrapper | None = None
        self._lock_code: int | None = None
        self._write_locks: list[FileLock] = []
        self._dependent_locks: list[FileLock] = []

    @property
    def file_path(self) -> Path:
        return self._file_path

    @property
    def locked(self) -> bool:
        return self._locked

    def _get_locked_write_lock_or_none(self) -> FileLock | None:
        if self._write_locks and any(lock.locked for lock in self._write_locks):
            return next(lock for lock in self._write_locks if lock.locked)
        return None

    def read_lock(self, *, non_blocking=False) -> FileLock:
        if self._fd is not None:
            raise ValueError("Can't get read lock when lock is already acquired")
        self_copy = copy.copy(self)
        self_copy._lock_code = fcntl.LOCK_SH  # noqa: SLF001
        self_copy._write_locks = self._write_locks  # noqa: SLF001
        if non_blocking:
            self_copy._lock_code |= fcntl.LOCK_NB  # noqa: SLF001
        return self_copy

    def write_lock(self, *, non_blocking=False) -> FileLock:
        if self._fd is not None:
            raise ValueError("Can't get read lock when lock is already acquired")
        self_copy = copy.copy(self)
        self_copy._lock_code = fcntl.LOCK_EX  # noqa: SLF001
        self_copy._write_locks = self._write_locks  # noqa: SLF001
        if non_blocking:
            self_copy._lock_code |= fcntl.LOCK_NB  # noqa: SLF001
        self._write_locks.append(self_copy)
        return self_copy

    def acquire(self) -> None:
        if self._lock_code is None:
            raise ValueError("Can't acquire bare lock, please use either read_lock or write_lock")

        self._fd = self._file_path.open()
        write_lock = self._get_locked_write_lock_or_none()
        if write_lock:
            write_lock._dependent_locks.append(self)  # noqa: SLF001
            self._locked = True
            return

        try:
            fcntl.flock(self._fd, self._lock_code)
            self._locked = True
        except BlockingIOError:
            # Release resources if we fail acquiring non-blocking lock
            self._fd.close()
            self._fd = None
            raise

    def release(self) -> None:
        if not self._fd:
            raise ValueError(f"Lock on {self._file_path} is not acquired and cannot be released")

        if self._lock_code in {fcntl.LOCK_EX, fcntl.LOCK_EX | fcntl.LOCK_NB} and self._dependent_locks:
            raise ValueError(
                "Found unreleased dependent lock, please release all read locks before releasing main write lock!",
            )

        self._locked = False
        write_lock = self._get_locked_write_lock_or_none()
        if write_lock:
            write_lock._dependent_locks.remove(self)  # noqa: SLF001
            return

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
            getattr(self, attr_name) == getattr(other, attr_name) for attr_name in ["_file_path", "_lock_code", "_fd"]
        )

    def __reduce__(self):
        if self._fd is not None:
            raise ValueError("Can't pickle lock when it's acquired, release lock before pickling")
        return self.__class__, (self._file_path,)
