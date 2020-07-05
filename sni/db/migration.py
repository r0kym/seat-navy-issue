"""
General database migration
"""

import logging
from typing import Callable, List

import sni.uac.migration as uac_migration
import sni.user.migration as user_migration


def migrate() -> None:
    """
    Runs various migration jobs on the database.

    Should be called immediately after initializing the connection.
    """
    migration_tasks: List[Callable[[], None]] = [
        user_migration.migrate_group,
        user_migration.migrate_user,
        user_migration.migrate_coalition,
        user_migration.ensure_root,
        user_migration.ensure_superuser_group,
        uac_migration.ensure_root_per_token,
        uac_migration.ensure_root_dyn_token,
    ]
    for task in migration_tasks:
        logging.info('Running database migration task %s', task.__name__)
        task()
