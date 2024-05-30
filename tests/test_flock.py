from concurrent import futures
from pathlib import Path
from time import sleep, time

import pytest

from replete.flock import FileLock

MAX_WORKERS = 16
NUM_INCREASE = 32
REQUIRED_TOTAL = MAX_WORKERS * NUM_INCREASE
TIMEOUT = 10


def _increase_file(path: Path) -> bool:
    lock = FileLock(path.parent / f"{path.name}.lock")
    for _ in range(NUM_INCREASE):
        with lock.write_lock(), path.open("r+") as f:
            last_line = f.readline().strip()
            f.seek(0)
            f.write(f"{int(last_line or 0) + 1}\n")
    return True


def _read_file(path: Path) -> bool:
    lock = FileLock(path.parent / f"{path.name}.lock")
    start = time()
    while time() < start + TIMEOUT:
        with lock.read_lock(), path.open("r+") as f:
            last_line = f.readline().strip()
            if last_line and int(last_line) == REQUIRED_TOTAL:
                return True
        sleep(0.01)  # Make sure writers have enough time to get the lock
    return False


@pytest.mark.parametrize("executor_cls", [futures.ThreadPoolExecutor, futures.ProcessPoolExecutor])
def test_parallel(tmp_path, executor_cls):
    path = tmp_path / "tmp.txt"
    with path.open("w") as f:
        f.write("0\n")
    with executor_cls(max_workers=MAX_WORKERS * 2) as executor:
        results = [executor.submit(_read_file, path) for _ in range(MAX_WORKERS)]
        results.extend([executor.submit(_increase_file, path) for _ in range(MAX_WORKERS)])
        futures.wait(results)
    assert len(results) == MAX_WORKERS * 2
    assert all(future.result() for future in results)


def test_read_read_reentrant(tmp_path):
    path = tmp_path / "tmp.txt"
    with path.open("w") as f:
        f.write("TEST\n")
    lock_path = path.parent / f"{path.name}.lock"
    with FileLock(lock_path).read_lock(), FileLock(lock_path).read_lock(), path.open("r") as f:
        assert f.read().strip() == "TEST"


def test_write_read_fail(tmp_path):
    path = tmp_path / "tmp.txt"
    with path.open("w") as f:
        f.write("TEST\n")
    lock_path = path.parent / f"{path.name}.lock"
    with (
        pytest.raises(BlockingIOError),
        FileLock(lock_path).write_lock(),
        FileLock(lock_path).read_lock(non_blocking=True),
        path.open("r") as f,
    ):
        assert f.read().strip() == "TEST"


def test_read_write_fail(tmp_path):
    path = tmp_path / "tmp.txt"
    with path.open("w") as f:
        f.write("TEST\n")
    lock_path = path.parent / f"{path.name}.lock"
    with (
        pytest.raises(BlockingIOError),
        FileLock(lock_path).read_lock(),
        FileLock(lock_path).write_lock(non_blocking=True),
        path.open("r") as f,
    ):
        assert f.read().strip() == "TEST"