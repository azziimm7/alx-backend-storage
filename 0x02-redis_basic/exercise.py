#!/usr/bin/env python3
"""A module that contains the Cache class"""
import redis
from uuid import uuid4
from typing import Union, Callable
from functools import wraps


def count_calls(method: Callable) -> Callable:
    """count number of method calls"""
    key = method.__qualname__

    @wraps(method)
    def wrapper(self, *args, **kwargs):
        """A wrapper around methods to count number of method calls"""
        self._redis.incr(key)
        return method(self, *args, **kwargs)
    return wrapper


def call_history(method: Callable) -> Callable:
    """Create a history for method calls"""
    key = method.__qualname__
    input_key = f'{key}:inputs'
    output_key = f'{key}:outputs'

    @wraps(method)
    def wrapper(self, *args, **kwargs):
        """A wrapper around methods to make a call history"""
        self._redis.rpush(input_key, str(args))
        output = str(method(self, *args, **kwargs))
        self._redis.rpush(output_key, output)
        return output
    return wrapper


def replay(method: Callable) -> None:
    """Replay the history of calls of a particular function"""
    r = redis.Redis()
    name = method.__qualname__
    inputs = r.lrange("{}:inputs".format(name), 0, -1)
    outputs = r.lrange("{}:outputs".format(name), 0, -1)
    print(f'{name} was called {len(outputs)} times:')
    for inp, out in zip(inputs, outputs):
        out = out.decode('utf-8')
        inp = inp.decode('utf-8')
        print(f'{name}(*{inp}) -> {out}')


class Cache:
    """A class that represent the caching mechanism"""

    def __init__(self):
        """Initialize the Cache class by creating a redis instance"""
        self._redis = redis.Redis()
        self._redis.flushdb()

    @count_calls
    @call_history
    def store(self, data: Union[str, bytes, int, float]) -> str:
        """Store a new value in the database"""
        key = str(uuid4())
        self._redis.set(key, data)
        return key

    def get(self, key: str,
            fn: Callable = None) -> Union[str, bytes, int, float]:
        """Get the value associated with this key in the database"""
        value = self._redis.get(key)
        if fn:
            return fn(value)
        return value

    def get_str(self, key: str) -> str:
        """Parametrize Cache.get with the str function"""
        return self._redis.get(key, str).decode("utf-8")

    def get_int(self, key: str) -> int:
        """Parametrize Cache.get with the int function"""
        return self._redis.get(key, int)
