import logging
import time
from functools import wraps
from typing import Callable, Any


def log_step(func: Callable) -> Callable:
    """
    Decorator to log the execution of a function, including its start, completion,
    duration, and any exceptions that occur.

    Args:
        func (Callable): The function to be decorated.

    Returns:
        Callable: The wrapped function with added logging.
    """

    @wraps(func)
    def wrapper(*args, **kwargs) -> Any:
        logging.info(f"Starting: {func.__name__}")
        start_time = time.time()
        try:
            result = func(*args, **kwargs)
            elapsed_time = time.time() - start_time
            logging.info(f"Completed: {func.__name__} in {elapsed_time:.2f} seconds")
            return result
        except Exception as e:
            logging.error(f"Error in {func.__name__}: {e}", exc_info=True)
            raise

    return wrapper
