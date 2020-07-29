"""
Some jobs to he scheduled, regarding the state of the database (e.g. making
sure all users are in the good corp, etc.)
"""

import logging

from sni.scheduler import scheduler

from .sso import refresh_access_token
from .token import EsiRefreshToken, save_esi_tokens


@scheduler.scheduled_job("interval", hours=1)
def refresh_tokens():
    """
    Iterates through the ESI refresh tokens and refreshes the corresponding ESI
    access tokens.
    """
    for refresh_token in EsiRefreshToken.objects(valid=True):
        usr = refresh_token.owner
        logging.debug(
            "Refreshing access token of character %d (%s)",
            usr.character_id,
            usr.character_name,
        )
        try:
            response = refresh_access_token(refresh_token.refresh_token)
            save_esi_tokens(response)
        except Exception as error:
            refresh_token.update(set__valid=False)
            logging.error(
                "Failed to refresh token of character %d (%s): %s",
                usr.character_id,
                usr.character_name,
                str(error),
            )
