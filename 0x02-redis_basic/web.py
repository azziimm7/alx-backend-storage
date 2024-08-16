#!/usr/bin/env python3
"""A module that contains the Cache class"""
import redis
import requests
from functools import wraps
from typing import Callable
from datetime import timedelta


r = redis.Redis()


def cache(fn: Callable) -> Callable:
    """Cache the get requests"""
    @wraps(fn)
    def wrapper(url):
        """A wrapper to cache the result of get equests"""
        r.incr(f'count:{url}')
        content = r.get('content: url')
        if content:
            return content.decode('utf-8')
        res = fn(url)
        r.set(f'count:{url}', 1)
        r.setex('content: url', 10, res)
        return res
    return wrapper


@cache
def get_page(url: str) -> str:
    """Obtain the HTML content of a particular URL and returns it"""
    res = requests.get(url)
    return res.content.decode('utf-8')
