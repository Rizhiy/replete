from __future__ import annotations

import asyncio
import itertools

import pytest

from nt_utils.aio import LazyWrapAsync


@pytest.mark.asyncio
async def test_lazy_wrap_async() -> None:

    counter = itertools.count()

    async def generate() -> int:
        return next(counter)

    generate_cached = LazyWrapAsync(generate)

    check_value = await generate()

    async def work() -> int:
        return await generate_cached()

    task_count = 30
    results = await asyncio.gather(*[work() for _ in range(task_count)])
    assert len(results) == task_count
    assert all(item == check_value + 1 for item in results)
    recheck_value = await generate()
    assert recheck_value == check_value + 2
