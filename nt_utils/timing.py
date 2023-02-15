from __future__ import annotations

import time
from collections import deque
from threading import Lock


class Timer:
    def __init__(self, base_time: float = None, include_sleep=False):
        self._base_time = base_time or self.__class__.get_sample_base_time()
        self._time_func = getattr(time, "perf_counter" if include_sleep else "process_time")

    @property
    def base_time(self) -> float:
        return self._base_time  # type: ignore

    def __enter__(self) -> Timer:
        self._start_time = self._time_func()
        return self

    def __exit__(self, *_):
        self._end_time = self._time_func()

    @property
    def time(self) -> float:
        return self._end_time - self._start_time

    @property
    def base_time_ratio(self) -> float:
        return self.time / self.base_time

    @classmethod
    def get_sample_base_time(cls, length=24, include_sleep=False) -> float:
        def dumb_fibonacci(n: int) -> int:
            if n < 2:
                return n
            return dumb_fibonacci(n - 1) + dumb_fibonacci(n - 2)

        with Timer(base_time=1, include_sleep=include_sleep) as t:
            dumb_fibonacci(length)

        return t.time


class RateLimiter:
    def __init__(self, max_weight: float, max_calls=None, period_length=1) -> None:
        self._max_weight = max_weight
        self._max_calls = max_calls
        self._period_seconds = period_length
        self._wait_lock = Lock()
        self._calls = deque()

    def check_rate(self, weight: float) -> None:
        with self._wait_lock:
            while not self._check_all():
                time.sleep(self._calls[0][1] - (time.time() - self._period_seconds))
            self._calls.append((weight, time.time()))

    def _weight_left(self) -> float:
        return self._max_weight - sum(c[0] for c in self._calls)

    def _clean_calls(self) -> None:
        while self._calls and self._calls[0][1] < time.time() - self._period_seconds:
            self._calls.popleft()

    def _check_calls(self) -> bool:
        return len(self._calls) < self._max_calls if self._max_calls else True

    def _check_weight(self) -> bool:
        return self._weight_left() > 0

    def _check_all(self) -> bool:
        self._clean_calls()
        return self._check_calls() and self._check_weight()