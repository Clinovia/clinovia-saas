# backend/app/core/cache.py

import functools
import hashlib
import json
from typing import Any, Callable, Dict

CacheType = Dict[str, Any]

_cache: CacheType = {}


# --------------------------------------------------
# Key generator
# --------------------------------------------------

def make_key(*parts: Any) -> str:
    """
    Generate deterministic cache key.
    """
    try:
        data = json.dumps(parts, sort_keys=True, default=str)
    except TypeError:
        data = str(parts)

    return hashlib.sha256(data.encode()).hexdigest()


# --------------------------------------------------
# Decorator
# --------------------------------------------------

def cache_result(func: Callable) -> Callable:
    """
    Decorator to cache function results in memory.
    """

    @functools.wraps(func)
    def wrapper(*args, **kwargs):

        key = make_key(func.__name__, args, kwargs)

        if key in _cache:
            return _cache[key]

        result = func(*args, **kwargs)

        _cache[key] = result

        return result

    return wrapper


# --------------------------------------------------
# Manual cache helpers
# --------------------------------------------------

def get_cached_prediction(key: str) -> Any:
    return _cache.get(key)


def set_cached_prediction(key: str, value: Any) -> None:
    _cache[key] = value


def clear_cache() -> None:
    _cache.clear()


def cache_size() -> int:
    return len(_cache)