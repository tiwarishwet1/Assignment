import time
from functools import wraps
from src.utils.logger import logger


def retry(
    max_attempts: int = 3,
    delay: float = 2.0,
    exceptions: tuple = (Exception,),
):
    """Retry decorator for resilient DOM interactions and HTTP calls."""

    def decorator(func):

        @wraps(func)
        def wrapper(*args, **kwargs):
            attempts = 0
            while attempts < max_attempts:
                try:
                    return func(*args, **kwargs)
                except exceptions as e:
                    attempts += 1
                    logger.warning(
                        f"Attempt {attempts}/{max_attempts} failed "
                        f"for '{func.__name__}': {e}"
                    )
                    if attempts == max_attempts:
                        raise e
                    time.sleep(delay)

        return wrapper

    return decorator
