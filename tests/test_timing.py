from __future__ import annotations

import random
import time

from flaky import flaky

from nt_utils import RateLimiter, Timer

SLEEP_TIME = 0.001


def test_sample_base_time():
    sample_base_time = Timer.get_sample_base_time()
    assert isinstance(sample_base_time, float)
    assert 0.001 < sample_base_time < 0.1


def test_basic_timer():
    with Timer() as t:
        Timer.get_sample_base_time()
    assert isinstance(t.time, float)
    assert t.time > 0


def test_sleep_timer():
    with Timer() as t:
        time.sleep(SLEEP_TIME)
    assert t.time < SLEEP_TIME / 10

    with Timer(include_sleep=True) as t:
        time.sleep(SLEEP_TIME)
    assert t.time > SLEEP_TIME


def test_base_time_ratio():
    with Timer(include_sleep=True) as t:
        time.sleep(SLEEP_TIME)
    ratio = t.base_time_ratio
    assert isinstance(ratio, float)

    with Timer(base_time=1.0, include_sleep=True) as t:
        time.sleep(SLEEP_TIME)
    assert t.base_time_ratio < ratio / 10


@flaky
def test_rate_limiter_weight():
    rate_limiter = RateLimiter(20, period_length=0.2)

    weights = [random.randint(3, 7) for _ in range(20)]
    with Timer(include_sleep=True) as t:
        for weight in weights:
            rate_limiter.check_rate(weight)
    # To make this test run fast, we allow some error in the rate
    assert t.time / 1.1 < (sum(weights) - 20) / 100 < t.time * 1.1


@flaky
def test_rate_limiter_num_calls():
    rate_limiter = RateLimiter(100, 5, 0.1)

    weights = [1] * 10
    with Timer(include_sleep=True) as t:
        for weight in weights:
            rate_limiter.check_rate(weight)
    assert t.time / 1.1 < 0.2 - 0.1 < t.time * 1.1
