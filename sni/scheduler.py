"""
Asyncronous / concurrent / schedules job management.

Simply use the global member ``sni.scheduler.scheduler``.

See also:
    `APScheduler documentation <https://apscheduler.readthedocs.io/en/stable/>`_
"""

from typing import Any, Callable

from apscheduler.executors.pool import ThreadPoolExecutor
from apscheduler.jobstores.redis import RedisJobStore
from apscheduler.schedulers.background import BackgroundScheduler

import sni.conf as conf
import sni.utils as utils

scheduler = BackgroundScheduler(
    executors={
        'default':
        ThreadPoolExecutor(conf.get('general.scheduler_thread_count')),
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
        'default': RedisJobStore(
            db=conf.get('redis.database'),
            host=conf.get('redis.host'),
            jobs_key='scheduler.default.jobs',
            port=conf.get('redis.port'),
            run_times_key='scheduler.default.run_times'
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
