"""
Various utilities
"""

import logging
from typing import Callable

from datetime import datetime, timedelta

from pytz import utc


# pylint: disable=dangerous-default-value
def catch_all(function: Callable,
              error_message: str,
              *,
              args: list = [],
              kwargs: dict = {}) -> None:
    """
    Calls a function but catches all the exceptions. If any were raised, logs
    an error message, followed by the string representation of the exception.
    """
    try:
        function(*args, **kwargs)
    except Exception as error:
        logging.error('%s: %s', error_message, str(error))


def from_timestamp(timestamp: int) -> datetime:
    """
    Returns a UTC datetime from a UNIX timestamp.
    """
    return datetime.utcfromtimestamp(timestamp)


def now() -> datetime:
    """
    Returns the current UTC datetime.
    """
    return datetime.now(utc)


def now_plus(**kwargs) -> datetime:
    """
    Returns the current UTC datetime plus a specified timedelta.

    See also:
        `datetime.timedelta <https://docs.python.org/3/library/datetime.html?highlight=timedelta#datetime.timedelta>`_
    """
    return now() + timedelta(**kwargs)
