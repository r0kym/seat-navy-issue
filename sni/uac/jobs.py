"""
Jobs
"""

import logging

from sni.scheduler import scheduler
from sni.user.models import Alliance, Corporation, User
from sni.user.user import ensure_user


@scheduler.scheduled_job("interval", hours=1)
def fix_ceo_clearance():
    """
    Raises CEOs of corporations to clearance level 2, and CEOs of alliances to
    level 4. If their clearance level was higher, doesn't modify it.
    """
    for corporation in Corporation.objects():
        ceo = ensure_user(corporation.ceo_character_id)
        if ceo.clearance_level < 2:
            logging.info(
                "Raising %s (%d), ceo of corporation %s (%d), to level 2",
                ceo.character_name,
                ceo.character_id,
                corporation.corporation_name,
                corporation.corporation_id,
            )
            ceo.update(set__clearance_level=2)
    for alliance in Alliance.objects():
        ceo: User = alliance.ceo
        if ceo.clearance_level < 4:
            logging.info(
                "Raising %s (%d), ceo of alliance %s (%d), to level 4",
                ceo.character_name,
                ceo.character_id,
                alliance.alliance_name,
                alliance.alliance_id,
            )
            ceo.update(set__clearance_level=4)
