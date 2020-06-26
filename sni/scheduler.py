"""
Asyncronous / concurrent / schedules job management.

Simply use the global member ``sni.scheduler.scheduler``.

See also:
    `APScheduler documentation <https://apscheduler.readthedocs.io/en/stable/>`_
"""

from apscheduler.executors.pool import ThreadPoolExecutor
from apscheduler.jobstores.memory import MemoryJobStore
from apscheduler.schedulers.background import BackgroundScheduler

import sni.conf as conf
import sni.time as time

scheduler = BackgroundScheduler(
    executors={
        'default':
        ThreadPoolExecutor(conf.get('general.scheduler_thread_count')),
    },
    job_defaults={
        'coalesce': False,
        'executor': 'default',
        'jobstore': 'default',
        'max_instances': 3,
        'misfire_grace_time': None,
    },
    jobstores={
        'default': MemoryJobStore(),
    },
    timezone=time.utc,
)
