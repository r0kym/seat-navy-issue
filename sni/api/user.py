"""
User management paths
"""

from datetime import datetime
from typing import List, Optional

from fastapi import (
    APIRouter,
    Depends,
    HTTPException,
    status,
)
import pydantic as pdt

from sni.esi.token import available_esi_scopes
from sni.uac.clearance import assert_has_clearance
from sni.uac.token import (
    from_authotization_header_nondyn,
    Token,
)
from sni.user.models import User

router = APIRouter()


class GetUserShortOut(pdt.BaseModel):
    """
    Model for an element of ``GET /user`` response
    """
    character_id: int
    character_name: str


class GetUserOut(pdt.BaseModel):
    """
    Model for ``GET /user/{character_name}`` responses
    """
    alliance: Optional[int]
    authorized_to_login: Optional[bool]
    available_esi_scopes: List[str]
    character_id: int
    character_name: str
    clearance_level: int
    coalitions: List[str]
    corporation: Optional[str]
    created_on: datetime
    cumulated_mandatory_esi_scopes: List[str]
    is_ceo_of_alliance: bool
    is_ceo_of_corporation: bool
    tickered_name: str
    updated_on: datetime


class PutUserIn(pdt.BaseModel):
    """
    Model for ``PUT /user/{character_id}`` requests
    """
    authorized_to_login: Optional[bool]
    clearance_level: Optional[int]


def user_record_to_response(usr: User) -> GetUserOut:
    """
    Populates a new :class:`sni.routers.user.GetUserOut` with the information
    contained in a user database record.
    """
    return GetUserOut(
        alliance=(usr.alliance.alliance_id
                  if usr.alliance is not None else None),
        authorized_to_login=usr.authorized_to_login,
        available_esi_scopes=available_esi_scopes(usr),
        character_id=usr.character_id,
        character_name=usr.character_name,
        clearance_level=usr.clearance_level,
        coalitions=[
            str(coalition.pk) for coalition in usr.coalitions()
        ],
        corporation=(usr.corporation.corporation_id
                     if usr.corporation is not None else None),
        created_on=usr.created_on,
        cumulated_mandatory_esi_scopes=usr.cumulated_mandatory_esi_scopes(),
        is_ceo_of_alliance=usr.is_ceo_of_alliance(),
        is_ceo_of_corporation=usr.is_ceo_of_corporation(),
        tickered_name=usr.tickered_name,
        updated_on=usr.updated_on,
    )


@router.get(
    '',
    response_model=List[GetUserShortOut],
    summary='Get the user list',
)
def get_user(tkn: Token = Depends(from_authotization_header_nondyn)):
    """
    Returns the list of all user names. Requires a clearance level of 0 or
    more.
    """
    assert_has_clearance(tkn.owner, 'sni.read_user')
    return [
        GetUserShortOut(
            character_id=usr.character_id,
            character_name=usr.character_name,
        ) for usr in User.objects()
    ]


@router.delete(
    '/{character_id}',
    summary='Delete a user',
)
def delete_user(character_id: int,
                tkn: Token = Depends(from_authotization_header_nondyn)):
    """
    Deletes a user. Requires a clearance level of 9 or more.
    """
    assert_has_clearance(tkn.owner, 'sni.delete_user')
    usr: User = User.objects.get(character_id=character_id)
    usr.delete()


@router.get(
    '/{character_id}',
    response_model=GetUserOut,
    summary='Get basic informations about a user',
)
def get_user_name(character_id: int,
                  tkn: Token = Depends(from_authotization_header_nondyn)):
    """
    Returns details about a character. Requires a clearance level of 0 or more.
    """
    assert_has_clearance(tkn.owner, 'sni.read_user')
    usr = User.objects.get(character_id=character_id)
    return user_record_to_response(usr)


@router.put(
    '/{character_id}',
    response_model=GetUserOut,
    summary='Update a user',
)
def put_user_name(character_id: int,
                  data: PutUserIn,
                  tkn: Token = Depends(from_authotization_header_nondyn)):
    """
    Manually updates non ESI data about a character. The required clearance
    level depends on the modification.
    """
    usr: User = User.objects.get(character_id=character_id)
    if data.clearance_level is not None:
        if not 0 <= data.clearance_level <= 10:
            raise HTTPException(
                status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail=
                'Field clearance_level must be between 0 and 10 (inclusive).')
        scope_name = f'sni.set_clearance_level_{data.clearance_level}'
        assert_has_clearance(tkn.owner, scope_name, usr)
        usr.clearance_level = data.clearance_level
    if data.authorized_to_login is not None:
        assert_has_clearance(tkn.owner, 'sni.set_authorized_to_login')
        usr.authorized_to_login = data.authorized_to_login
    usr.save()
    return user_record_to_response(usr)
