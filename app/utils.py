import time
import logging

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def retry(max_retries: int = 3, delay: int = 2):
    def decorator(func):
        def wrapper(*args, **kwargs):
            retries = 0
            while retries < max_retries:
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    retries += 1
                    logger.warning(f"Retry {retries}/{max_retries} for {func.__name__}: {e}")
                    if retries >= max_retries:
                        logger.error(f"Max retries reached for {func.__name__}")
                        raise
                    time.sleep(delay)
        return wrapper
    return decorator
