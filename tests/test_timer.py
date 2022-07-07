from __future__ import annotations

import time

from nt_utils import Timer

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
