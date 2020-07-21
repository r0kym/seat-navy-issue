"""
Asyncronous / concurrent / schedules job management.

Simply use the global member ``sni.scheduler.scheduler``.

See also:
    `APScheduler documentation <https://apscheduler.readthedocs.io/en/stable/>`_
"""

import logging
from typing import Any, Callable

from apscheduler.executors.pool import ThreadPoolExecutor
from apscheduler.jobstores.redis import RedisJobStore
from apscheduler.schedulers.background import BackgroundScheduler

from sni.db.redis import new_redis_connection
import sni.conf as conf
import sni.utils as utils

ENABLED: bool = True
"""Wether the scheduler is enabled"""

JOBS_KEY: str = 'scheduler.default.jobs'
"""The redis key for the job list"""

RUN_TIMES_KEY: str = 'scheduler.default.run_times'
"""The redis key for the job run times"""

scheduler = BackgroundScheduler(
    executors={
        'default': ThreadPoolExecutor(
            conf.get('general.scheduler_thread_count'),
        ),
    },
    job_defaults={
        'coalesce': True,
        'executor': 'default',
        'jitter': 60,
        'jobstore': 'default',
        'max_instances': 3,
        'misfire_grace_time': None,
    },
    jobstores={
        'default':
        RedisJobStore(
            db=conf.get('redis.database'),
            host=conf.get('redis.host'),
            jobs_key=JOBS_KEY,
            port=conf.get('redis.port'),
            run_times_key=RUN_TIMES_KEY,
        ),
    },
    timezone=utils.utc,
)


# pylint: disable=dangerous-default-value
def add_job(func: Callable, args=list(), kwargs=dict(), **kw):
    """
    Adds a job to the scheduler. If the scheduler is disable, runs the job
    immediately.
    """
    if ENABLED:
        scheduler.add_job(func, args=args, kwargs=kwargs, **kw)
    else:
        func(*args, **kwargs)


def run_scheduled(function: Callable) -> Callable:
    """
    Decorator that makes a function scheduled to run immediately when called.

    Example::

        @signals.post_save.connect_via(User)
        @run_scheduled
        def test(_sender: Any, **kwargs):
            usr = kwargs['document']
            status = 'created' if kwargs.get('created', False) else 'updated'
            logging.debug('User %s has been %s', status, usr.character_name)

    """
    def wrapper(sender: Any, **kwargs):
        scheduler.add_job(function, args=(sender, ), kwargs=kwargs)

    return wrapper


def start_scheduler() -> None:
    """
    Clears the job store and starts the scheduler.
    """
    if not ENABLED:
        logging.warning("Not starting the scheduler since it is disabled")
        return
    redis = new_redis_connection()
    redis.delete(JOBS_KEY, RUN_TIMES_KEY)
    scheduler.start()


def stop_scheduler() -> None:
    """
    Stops the scheduler and cleans up things
    """
    scheduler.shutdown()
