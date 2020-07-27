"""
Asyncronous / concurrent / schedules job management.

Simply use the global member ``sni.scheduler.scheduler``.

See also:
    `APScheduler documentation <https://apscheduler.readthedocs.io/en/stable/>`_
"""

from typing import Any, Callable
import logging

from apscheduler.executors.pool import ThreadPoolExecutor
from apscheduler.jobstores.redis import RedisJobStore
from apscheduler.schedulers.background import BackgroundScheduler

from sni.db.redis import new_redis_connection
from sni.conf import CONFIGURATION as conf
import sni.utils as utils

JOBS_KEY: str = 'scheduler.default.jobs'
"""The redis key for the job list"""

RUN_TIMES_KEY: str = 'scheduler.default.run_times'
"""The redis key for the job run times"""

scheduler = BackgroundScheduler(
    executors={
        'default': ThreadPoolExecutor(conf.general.scheduler_thread_count, ),
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
            db=conf.redis.database,
            host=conf.redis.host,
            jobs_key=JOBS_KEY,
            port=conf.redis.port,
            run_times_key=RUN_TIMES_KEY,
        ),
    },
    timezone=utils.utc,
)


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
    redis = new_redis_connection()
    scheduler.remove_all_jobs()
    redis.delete(JOBS_KEY, RUN_TIMES_KEY)
    scheduler.start()
    logging.debug('Started scheduler')


def stop_scheduler() -> None:
    """
    Stops the scheduler and cleans up things
    """
    scheduler.shutdown()
    logging.debug('Stopped scheduler')


def _test_tick() -> None:
    """
    Test function to check that the scheduler is really running.

    Schedule like this::

        scheduler.add_job(_test_tick, 'interval', seconds=3, jitter=0)

    """
    logging.debug('Tick!')
    scheduler.add_job(_test_tock)


def _test_tock() -> None:
    """
    Test function to check that the scheduler is really running.
    """
    logging.debug('Tock!')
