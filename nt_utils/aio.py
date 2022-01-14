from __future__ import annotations

import asyncio
from typing import Awaitable, Callable, Optional, TypeVar

TLazyWrapValue = TypeVar("TLazyWrapValue")


class LazyWrapAsync:
    def __init__(self, generate: Callable[[], Awaitable[TLazyWrapValue]]) -> None:
        self._generate = generate
        self._generate_done = False
        self._value: Optional[TLazyWrapValue] = None
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
