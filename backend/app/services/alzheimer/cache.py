"""
Optional in-memory cache for repeated predictions.
Provides decorator `cache_result` and helper functions for manual cache access.
"""

import functools
import hashlib
import json
from typing import Any, Callable, Dict

_cache: Dict[str, Any] = {}


def _make_key(*args, **kwargs) -> str:
    """Generate a deterministic key based on function arguments."""
    try:
        data = json.dumps({"args": args, "kwargs": kwargs}, sort_keys=True, default=str)
    except TypeError:
        data = str((args, kwargs))
    return hashlib.sha256(data.encode()).hexdigest()


def cache_result(func: Callable):
    """Simple in-memory caching decorator for expensive computations."""
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        key = _make_key(func.__name__, *args, **kwargs)
        if key in _cache:
            return _cache[key]
        result = func(*args, **kwargs)
        _cache[key] = result
        return result
    return wrapper


def get_cached_prediction(key: str):
    """Manually retrieve a cached value by key."""
    return _cache.get(key)


def set_cached_prediction(key: str, value: dict):
    """Manually set a cache entry."""
    _cache[key] = value


def clear_cache():
    """Clear all cached results."""
    _cache.clear()
