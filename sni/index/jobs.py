"""
Scheduled indexaction jobs
"""

import re

from sni.esi.token import esi_get_on_befalf_of, has_esi_scope
from sni.scheduler import scheduler
from sni.user.models import User

from .models import EsiMail, EsiMailRecipient


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
        f'latest/characters/{character_id}/mail/{mail_id}', character_id).json()
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
            scheduler.add_job(index_user_mails, args=(usr, ))


def format_mail_body(body: str) -> str:
    """
    Formats a mail body by removing most of the HTML tags.
    """
    body = body.replace('<br>', '\n')
    body = re.sub('</\w+>', '', body)
    body = re.sub('<font[^>]*>', '', body)
    body = re.sub('<a href[^>]*>', '', body)
    return body
