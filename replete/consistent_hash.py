from __future__ import annotations

import collections.abc
import contextlib
import datetime
import pickle  # noqa S403, not loading anything here, only dumping
from typing import TYPE_CHECKING

import xxhash

if TYPE_CHECKING:
    from collections.abc import Callable, Sequence
    from typing import Any

# Bitmask value to cap the hash intdigest, so that no overflow occurs when it
# passes through the `hash()` builtin.
INT64_MAX = 2**63 - 1

PRIMITIVE_TYPES = frozenset(
    (
        bytes,
        str,
        int,
        bool,
        float,
        # Using `repr` on `datetime` is actually relatively fast (~1.5 microseconds);
        # the only possibly faster way is making a tuple out of its attributes (~1 microsecond into a string).
        # And pickling is very slow for `tzinfo` (~25 microseconds).
        # `.timestamp()` is around ~5 microseconds with timezone.
        datetime.datetime,
    ),
)


def consistent_hash_raw_update(
    hasher: xxhash.xxh3_64,
    params: Sequence[Any] = (),
    primitive_types: frozenset[type] = PRIMITIVE_TYPES,
    *,
    type_name_dependence: bool = False,
    try_pickle: bool = True,
) -> None:
    for param in params:
        param_type = param.__class__
        if type_name_dependence:
            hasher.update(b"\x00")
            hasher.update(param_type.__name__.encode())
        if param_type is bytes:
            hasher.update(b"\x01")
            hasher.update(param)
        elif param_type in primitive_types:
            hasher.update(b"\x02")
            hasher.update(repr(param).encode())
        elif (chashmeth := getattr(param, "_consistent_hash", None)) is not None and getattr(
            chashmeth,
            "__self__",
            None,
        ) is not None:
            rec_int = chashmeth()
            hasher.update(b"\x03")
            hasher.update(rec_int.to_bytes(8, "big"))
        elif param_type is dict or isinstance(param, collections.abc.Mapping):
            param_items = sorted((str(key), value) for key, value in param.items())
            hasher.update(b"\x04")
            consistent_hash_raw_update(hasher, param_items)
        elif param_type is list or param_type is tuple or isinstance(param, list | tuple):
            hasher.update(b"\x05")
            consistent_hash_raw_update(hasher, param)
        else:
            param_bytes = None
            if try_pickle:
                with contextlib.suppress(Exception):
                    param_bytes = pickle.dumps(param)
            if param_bytes is not None:
                hasher.update(b"\x06")
                hasher.update(param_bytes)
            else:
                param_bytes = repr(param).encode()  # Dangerous fallback.
                hasher.update(b"\x07")
                hasher.update(param_bytes)


def consistent_hash(*args: Any, **kwargs: Any) -> int:
    hasher = xxhash.xxh3_64()
    params = [*args, *sorted(kwargs.items())] if kwargs else args
    consistent_hash_raw_update(hasher, params)
    return hasher.intdigest() & INT64_MAX


def _normalize(value: Any) -> Any:
    value_type = type(value)
    if value_type in PRIMITIVE_TYPES:
        return value
    chashmeth = getattr(value, "consistent_hash", None)
    if chashmeth is not None and getattr(chashmeth, "__self__", None) is not None:
        return chashmeth()  # Note: makes the result type-independent.
    if value_type is list or value_type is tuple or isinstance(value, list | tuple):
        return [_normalize(subvalue) for subvalue in value]
    if value_type is dict or isinstance(value, collections.abc.Mapping):
        res_value = [(str(subkey), _normalize(subvalue)) for subkey, subvalue in value.items()]
        res_value.sort()
        return res_value
    return value


def picklehash(value: Any, normalizer: Callable[[Any], Any] | None = _normalize) -> int:
    value_norm = normalizer(value) if normalizer is not None else value
    value_b = pickle.dumps(value_norm, protocol=5)
    return xxhash.xxh3_64_intdigest(value_b) & INT64_MAX
