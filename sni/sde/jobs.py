"""
Recurrent SDE jobs
"""

import logging

from sni.scheduler import scheduler
from sni.db.redis import new_connection
import sni.utils as utils

from .sde import (
    download_latest_sde,
    get_latest_sde_md5,
    import_sde_dump,
)


@scheduler.scheduled_job('interval',
                         days=1,
                         start_date=utils.now_plus(minutes=10))
def update_sde() -> None:
    """
    Checks the hash of the SDE, and if needed, downloads and imports it.
    """
    redis = new_connection()
    latest_sde_md5 = get_latest_sde_md5()
    current_sde_md5 = redis.get('sde_md5')
    if current_sde_md5 is not None:
        current_sde_md5 = current_sde_md5.decode()
    if latest_sde_md5 == current_sde_md5:
        logging.debug('SDE is up to date')
        return
    logging.debug('SDE is out of date')
    dump_path = 'sde.sqlite'
    download_latest_sde(dump_path)
    import_sde_dump(dump_path)
    redis.set('sde_md5', latest_sde_md5)
