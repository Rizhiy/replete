from __future__ import annotations

import asyncio
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from collections.abc import AsyncIterable, Awaitable, Callable
    from typing import TypeVar

    T = TypeVar("T")
    TLazyWrapValue = TypeVar("TLazyWrapValue")


async def achunked(aiterable: AsyncIterable[T], size: int) -> AsyncIterable[list[T]]:
    """Async iterable chunker"""
    chunk: list[T] = []
    async for item in aiterable:
        chunk.append(item)
        if len(chunk) >= size:
            yield chunk
            chunk = []
    if chunk:
        yield chunk


class LazyWrapAsync:
    def __init__(self, generate: Callable[[], Awaitable[TLazyWrapValue]]) -> None:
        self._generate = generate
        self._generate_done = False
        self._value: TLazyWrapValue
        self._write_lock = asyncio.Lock()

    async def __call__(self) -> TLazyWrapValue:
        # Pre-check to avoid locking each and every read.
        if self._generate_done:
            return self._value
        async with self._write_lock:
            # Re-check in case another task generated the value.
            if self._generate_done:
                return self._value

            value = await self._generate()
            self._value = value
            self._generate_done = True
            return value
