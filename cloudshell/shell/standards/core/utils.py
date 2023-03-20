from __future__ import annotations

import functools
import re
from collections.abc import Iterator

COLLECTION_SEPARATOR_PATTERN = re.compile(r"[,;]")


def attr_length_validator(max_length: int):
    def decorator_func(func):
        @functools.wraps(func)
        def inner(*args, **kwargs):
            nargs = []
            for arg in args:
                if isinstance(arg, str):
                    nargs.append(arg[:max_length])
                else:
                    nargs.append(arg)

            for key, value in kwargs.items():
                if isinstance(value, str):
                    kwargs[key] = value[:max_length]

            return func(*nargs, **kwargs)

        return inner

    return decorator_func


def split_list_of_values(string: str) -> Iterator[str, None, None]:
    return filter(bool, map(str.strip, COLLECTION_SEPARATOR_PATTERN.split(string)))
