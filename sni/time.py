"""
Datetime utilities
"""
from datetime import datetime, timedelta

from pytz import utc


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
