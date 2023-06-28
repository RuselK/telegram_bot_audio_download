import functools
import logging


def log(logger: logging.Logger):
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            logger.debug(f'Calling function {func.__name__}')
            logger.debug(f'Arguments: {args}, {kwargs}')
            result = func(*args, **kwargs)
            logger.debug(f'Function {func.__name__} returned {result}')
            return result
        return wrapper
    return decorator
