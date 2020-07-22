"""
Scheduled indexaction jobs
"""

import html
import re

from sni.esi.token import esi_get_on_befalf_of, has_esi_scope
from sni.scheduler import scheduler
from sni.user.models import User

from .models import (
    EsiCharacterLocation,
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


def index_user_location(usr: User):
    """
    Indexes a user's location, online status, and ship
    """
    location_data = esi_get_on_befalf_of(
        f'latest/characters/{usr.character_id}/location/',
        usr.character_id,
    ).data
    online_data = esi_get_on_befalf_of(
        f'latest/characters/{usr.character_id}/online/',
        usr.character_id,
    ).data
    ship_data = esi_get_on_befalf_of(
        f'latest/characters/{usr.character_id}/ship/',
        usr.character_id,
    ).data
    EsiCharacterLocation(
        online=online_data['online'],
        ship_item_id=ship_data['ship_item_id'],
        ship_name=ship_data['ship_name'],
        ship_type_id=ship_data['ship_type_id'],
        solar_system_id=location_data['solar_system_id'],
        station_id=location_data.get('station_id'),
        structure_id=location_data.get('structure_id'),
        user=usr,
    ).save()


@scheduler.scheduled_job('interval', hours=1)
def index_users_location():
    """
    Indexes all user's location
    """
    for usr in User.objects():
        if has_esi_scope(usr, 'esi-location.read_location.v1') and \
            has_esi_scope(usr, 'esi-location.read_online.v1') and \
            has_esi_scope(usr, 'esi-location.read_ship_type.v1'):
            scheduler.add_job(index_user_location, args=(usr, ))


def index_user_mails(usr: User):
    """
    Pulls a character's email
    """
    character_id = usr.character_id
    for header in esi_get_on_befalf_of(
            f'latest/characters/{character_id}/mail', character_id).data:
        mail_id = header['mail_id']
        if EsiMail.objects(mail_id=mail_id).first() is not None:
            break
        mail = esi_get_on_befalf_of(
            f'latest/characters/{character_id}/mail/{mail_id}',
            character_id).data
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


def measure_user_skillpoints(usr: User):
    """
    Measures a user's skillpoints. See
    :class:`sni.index.models.EsiSkillPoints`.
    """
    data = esi_get_on_befalf_of(
        f'latest/characters/{usr.character_id}/skills/',
        usr.character_id,
    ).data
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
            scheduler.add_job(measure_user_skillpoints, args=(usr, ))
