import time
import functools
from typing import Callable, Any


def async_timed(func: Callable) -> Callable:
    """Decorator to time an async function."""

    @functools.wraps(func)
    async def wrapper(*args, **kwargs) -> Any:
        start = time.perf_counter()
        try:
            return await func(*args, **kwargs)
        finally:
            end = time.perf_counter()
            total = end - start
            print(f"Function '{func.__name__}' took {total:.4f} seconds to complete.")

    return wrapper
