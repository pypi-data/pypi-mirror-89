# -*- coding: utf-8 -*-

from functools import wraps
from typing import Any, Callable, TypeVar, cast

from simplethread.thread import mutex
from simplethread.thread import start

__all__ = ("synchronized", "threaded")

_F = TypeVar("_F", bound=Callable[..., Any])


def synchronized(user_function: _F) -> _F:
    """
    A decorator to synchronize a ``user_function``.
    """
    @wraps(user_function)
    def wrapper(*args: Any, **kwargs: Any) -> Any:
        with mutex:
            return user_function(*args, **kwargs)

    return cast(_F, wrapper)


def threaded(user_function: _F) -> Callable[..., int]:
    """
    A decorator to run a ``user_function`` in a separate thread.
    """
    @wraps(user_function)
    def wrapper(*args: Any, **kwargs: Any) -> int:
        return start(user_function, args, kwargs)

    return wrapper
