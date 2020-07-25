"""
Some jobs to he scheduled, regarding the state of the database (e.g. making
sure all users are in the good corp, etc.)
"""

from sni.scheduler import scheduler
import sni.utils as utils

from .sso import refresh_access_token
from .token import EsiRefreshToken, save_esi_tokens


@scheduler.scheduled_job('interval', hours=1)
def refresh_tokens():
    """
    Iterates through the ESI refresh tokens and refreshes the corresponding ESI
    access tokens.
    """
    for refresh_token in EsiRefreshToken.objects(valid=True):
        usr = refresh_token.owner
        utils.catch_all(
            save_esi_tokens,
            f'Could not refresh access token of user {usr.character_name}',
            args=[refresh_access_token(refresh_token.refresh_token)],
        )
