"""
Asyncronous / concurrent / schedules job management.
"""

from apscheduler.executors.pool import ProcessPoolExecutor
from apscheduler.jobstores.memory import MemoryJobStore
from apscheduler.schedulers.background import BackgroundScheduler

import sni.conf as conf
import sni.time as time

scheduler = BackgroundScheduler(
    executors={
        'default':
        ProcessPoolExecutor(conf.get('general.scheduler_process_count')),
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
