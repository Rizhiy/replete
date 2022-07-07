from __future__ import annotations

import time


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
