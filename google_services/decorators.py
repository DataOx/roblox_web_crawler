import time
from random import randint
from functools import wraps

from googleapiclient.errors import HttpError
from httplib2 import ServerNotFoundError

from google_services.connections import logger
from config import GOOGLE_MIN_BACKOFF_TIME, GOOGLE_MAX_BACKOFF_TIME


def retry_with_backoff(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        minimum_backoff_time = GOOGLE_MIN_BACKOFF_TIME
        pipe_err_count = 0
        while True:
            try:
                return func(*args, **kwargs)
            except (ConnectionResetError, ServerNotFoundError):
                time.sleep(5)
                continue
            except BrokenPipeError as bpe:
                time.sleep(5)
                pipe_err_count += 1
                if pipe_err_count == 2:
                    raise bpe
            except HttpError as http_error:
                if http_error.status_code != 429:
                    raise http_error
                print(http_error.resp)
                print(http_error.content)
                if minimum_backoff_time > GOOGLE_MAX_BACKOFF_TIME:
                    raise http_error
                delay = minimum_backoff_time + randint(0, 1000) / 1000.0
                msg = 'Error 429 backoff delay is {delay}...'
                logger.warning(msg)
                print(f'{logger.name} {msg}')
                time.sleep(delay)
                minimum_backoff_time *= 2
    return wrapper
