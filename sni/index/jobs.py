"""
Scheduled indexaction jobs
"""

import html
import re

from sni.esi.token import esi_get_on_befalf_of, has_esi_scope
from sni.scheduler import add_job, scheduler
from sni.user.models import User

from .models import (
    EsiMail,
    EsiMailRecipient,
    EsiSkillPoints,
)


def format_mail_body(body: str) -> str:
    """
    Formats a mail body by removing most of the HTML tags.
    """
    body = body.replace('<br>', '\n')
    body = re.sub(r'<.*?>', '', body)
    body = html.unescape(body)
    return body


def index_user_mails(usr: User):
    """
    Pulls a character's email
    """
    character_id = usr.character_id
    for header in esi_get_on_befalf_of(
            f'latest/characters/{character_id}/mail', character_id).json():
        mail_id = header['mail_id']
        if EsiMail.objects(mail_id=mail_id).first() is not None:
            break
        mail = esi_get_on_befalf_of(
            f'latest/characters/{character_id}/mail/{mail_id}',
            character_id).json()
        EsiMail(
            body=format_mail_body(mail['body']),
            from_id=mail['from'],
            mail_id=mail_id,
            recipients=[EsiMailRecipient(**raw) for raw in mail['recipients']],
            subject=mail['subject'],
            timestamp=mail['timestamp'],
        ).save()


@scheduler.scheduled_job('interval', hours=1)
def index_users_mails():
    """
    Index all user emails.
    """
    for usr in User.objects():
        if has_esi_scope(usr, 'esi-mail.read_mail.v1'):
            add_job(index_user_mails, args=(usr, ))


def measure_user_skillpoints(usr: User):
    """
    Measures a user's skillpoints. See
    :class:`sni.index.models.EsiSkillPoints`.
    """
    data = esi_get_on_befalf_of(
        f'latest/characters/{usr.character_id}/skills/',
        usr.character_id,
    ).json()
    EsiSkillPoints(
        total_sp=data['total_sp'],
        unallocated_sp=data.get('unallocated_sp', 0),
        user=usr,
    ).save()


@scheduler.scheduled_job('interval', hours=12)
def measure_users_skillpoints():
    """
    Measures all users skillpoints
    """
    for usr in User.objects():
        if has_esi_scope(usr, 'esi-skills.read_skills.v1'):
            add_job(measure_user_skillpoints, args=(usr, ))
