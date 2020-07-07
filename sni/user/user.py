"""
User (aka character), corporation, and alliance management
"""

from sni.esi.esi import esi_get

from .models import (
    Alliance,
    Corporation,
    Group,
    User,
)


def ensure_alliance(alliance_id: int) -> Alliance:
    """
    Ensures that an alliance exists, and returns it. It it does not, creates
    it by fetching relevant data from the ESI.
    """
    alliance = Alliance.objects(alliance_id=alliance_id).first()
    if alliance is None:
        data = esi_get(f'latest/alliances/{alliance_id}').json()
        alliance = Alliance(
            alliance_id=alliance_id,
            alliance_name=data['name'],
            executor_corporation_id=int(data['executor_corporation_id']),
            ticker=data['ticker'],
        ).save()
    return alliance


def ensure_autogroup(name: str) -> Group:
    """
    Ensured that an automatically created group exists. Automatic groups are
    owned by root.
    """
    grp = Group.objects(group_name=name).first()
    if grp is None:
        root = User.objects.get(character_id=0)
        grp = Group(
            is_autogroup=True,
            members=[root],
            group_name=name,
            owner=root,
        ).save()
    return grp


def ensure_corporation(corporation_id: int) -> Corporation:
    """
    Ensures that a corporation exists, and returns it. It it does not, creates
    it by fetching relevant data from the ESI.
    """
    corporation = Corporation.objects(corporation_id=corporation_id).first()
    if corporation is None:
        data = esi_get(f'latest/corporations/{corporation_id}').json()
        alliance = ensure_alliance(
            data['alliance_id']) if 'alliance_id' in data else None
        corporation = Corporation(
            alliance=alliance,
            ceo_character_id=int(data['ceo_id']),
            corporation_id=corporation_id,
            corporation_name=data['name'],
            ticker=data['ticker'],
        ).save()
    return corporation


def ensure_user(character_id: int) -> User:
    """
    Ensures that a user (with a valid ESI character ID) exists, and returns it.
    It it does not, creates it by fetching relevant data from the ESI. Also
    creates the character's corporation and alliance (if applicable).
    """
    usr = User.objects(character_id=character_id).first()
    if usr is None:
        data = esi_get(f'latest/characters/{character_id}').json()
        usr = User(
            character_id=character_id,
            character_name=data['name'],
            corporation=ensure_corporation(data['corporation_id']),
        ).save()
    return usr
