from __future__ import annotations

import collections.abc
import datetime
import pickle
from collections.abc import Sequence
from typing import Any, cast

import xxhash

PRIMITIVE_TYPE_NAMES = frozenset(
    cls.__name__
    for cls in (
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
    )
)


def consistent_hash_raw(
    args: Sequence[Any] = (),
    kwargs: dict[str, Any] = None,
    primitive_type_names=PRIMITIVE_TYPE_NAMES,
    type_name_dependence=False,
    try_pickle=True,
) -> xxhash.xxh128:
    params = [*args, *sorted(kwargs.items())] if kwargs else args
    hasher = xxhash.xxh128()
    for param in params:
        type_name = param.__class__.__name__
        if type_name in primitive_type_names:
            if type_name == "bytes":
                param_bytes = param
            else:
                param_bytes = repr(param).encode()
        elif chashmeth := getattr(param, "_consistent_hash", None):
            rec_int = chashmeth()
            param_bytes = rec_int.to_bytes(16, "little")
        elif isinstance(param, collections.abc.Mapping):
            param_items = {str(key): value for key, value in param.items()}
            param_bytes = consistent_hash_raw((), param_items).digest()
        elif isinstance(param, (list, tuple)):
            param_bytes = consistent_hash_raw(param).digest()
        else:
            param_bytes = None
            if try_pickle:
                try:
                    param_bytes = pickle.dumps(param)
                except Exception:
                    pass
            if param_bytes is None:
                param_bytes = repr(param).encode()  # Dangerous fallback.
        if type_name_dependence:
            hasher.update(b"\x00")
            hasher.update(type_name.encode())
            hasher.update(b"\x00")
        hasher.update(param_bytes)
    return hasher


def consistent_hash(*args, **kwargs) -> int:
    return cast(int, consistent_hash_raw(args, kwargs).intdigest())
