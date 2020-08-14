"""
Scheduled indexaction jobs
"""

import logging
import html
import re

from sni.esi.token import esi_get_on_befalf_of, has_esi_scope
from sni.scheduler import scheduler
from sni.user.models import User

from .index import get_user_location
from .models import (
    EsiMail,
    EsiMailRecipient,
    EsiSkillPoints,
    EsiWalletBalance,
)


def format_mail_body(body: str) -> str:
    """
    Formats a mail body by removing most of the HTML tags.
    """
    body = body.replace("<br>", "\n")
    body = re.sub(r"<.*?>", "", body)
    body = html.unescape(body)
    return body


def index_user_location(usr: User):
    """
    Indexes a user's location, online status, and ship
    """
    try:
        location = get_user_location(usr, invalidate_token_on_error=True)
        location.save()
    except Exception as error:
        logging.error(
            "Could not index location of character %d (%s): %s",
            usr.character_id,
            usr.character_name,
            str(error),
        )


@scheduler.scheduled_job("interval", hours=1)
def index_users_location():
    """
    Indexes all user's location
    """
    for usr in User.objects():
        if (
            has_esi_scope(usr, "esi-location.read_location.v1")
            and has_esi_scope(usr, "esi-location.read_online.v1")
            and has_esi_scope(usr, "esi-location.read_ship_type.v1")
        ):
            scheduler.add_job(index_user_location, args=(usr,))


def index_user_mails(usr: User):
    """
    Pulls a character's email
    """
    try:
        character_id = usr.character_id
        headers = esi_get_on_befalf_of(
            f"latest/characters/{character_id}/mail",
            character_id,
            invalidate_token_on_error=True,
            raise_for_status=True,
        ).data
    except Exception as error:
        logging.error(
            "Could not list recent emails of character %d (%s): %s",
            usr.character_id,
            usr.character_name,
            str(error),
        )
    for header in headers:
        mail_id = header["mail_id"]
        if EsiMail.objects(mail_id=mail_id).first() is not None:
            break
        try:
            mail = esi_get_on_befalf_of(
                f"latest/characters/{character_id}/mail/{mail_id}",
                character_id,
                invalidate_token_on_error=True,
                raise_for_status=True,
            ).data
            EsiMail(
                body=format_mail_body(mail["body"]),
                from_id=mail["from"],
                mail_id=mail_id,
                recipients=[
                    EsiMailRecipient(**raw) for raw in mail["recipients"]
                ],
                subject=mail["subject"],
                timestamp=mail["timestamp"],
            ).save()
        except Exception as error:
            logging.error(
                "Could not index mail %d from character %d (%s): %s",
                mail_id,
                usr.character_id,
                usr.character_name,
                str(error),
            )


@scheduler.scheduled_job("interval", hours=1)
def index_users_mails():
    """
    Index all user emails.
    """
    for usr in User.objects():
        if has_esi_scope(usr, "esi-mail.read_mail.v1"):
            scheduler.add_job(index_user_mails, args=(usr,))


def index_user_skillpoints(usr: User):
    """
    Measures a user's skillpoints. See
    :class:`sni.index.models.EsiSkillPoints`.
    """
    try:
        data = esi_get_on_befalf_of(
            f"latest/characters/{usr.character_id}/skills/",
            usr.character_id,
            invalidate_token_on_error=True,
            raise_for_status=True,
        ).data
        EsiSkillPoints(
            total_sp=data["total_sp"],
            unallocated_sp=data.get("unallocated_sp", 0),
            user=usr,
        ).save()
    except Exception as error:
        logging.error(
            "Could not index skillpoints of character %d (%s): %s",
            usr.character_id,
            usr.character_name,
            str(error),
        )


@scheduler.scheduled_job("interval", hours=12)
def index_users_skillpoints():
    """
    Measures all users skillpoints
    """
    for usr in User.objects():
        if has_esi_scope(usr, "esi-skills.read_skills.v1"):
            scheduler.add_job(index_user_skillpoints, args=(usr,))


def index_user_wallets(usr: User):
    """
    Indexes user wallet balance
    """
    try:
        balance = esi_get_on_befalf_of(
            f"latest/characters/{usr.character_id}/wallet/",
            usr.character_id,
            invalidate_token_on_error=True,
            raise_for_status=True,
        ).data
        EsiWalletBalance(balance=balance, user=usr).save()
    except Exception as error:
        logging.error(
            "Could not index wallet of character %d (%s): %s",
            usr.character_id,
            usr.character_name,
            str(error),
        )


@scheduler.scheduled_job("interval", hours=12)
def index_users_wallets():
    """
    Indexes user wallet balance
    """
    for usr in User.objects():
        if has_esi_scope(usr, "esi-wallet.read_character_wallet.v1"):
            scheduler.add_job(index_user_wallets, args=(usr,))
