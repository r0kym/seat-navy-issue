"""
Some jobs to he scheduled, regarding the state of the database (e.g. making
sure all users are in the good corp, etc.)
"""

from sni.scheduler import scheduler
import sni.esi.sso as sso
import sni.esi.token as esitoken
import sni.utils as utils


@scheduler.scheduled_job('interval', hours=1)
def refresh_tokens():
    """
    Iterates through the ESI refresh tokens and refreshes the corresponding ESI
    access tokens.
    """
    for refresh_token in esitoken.EsiRefreshToken.objects():
        usr = refresh_token.owner
        utils.catch_all(
            esitoken.save_esi_tokens,
            f'Could not refresh access token of user {usr.character_name}',
            args=[sso.refresh_access_token(refresh_token.refresh_token)],
        )
