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

import sni.uac.clearance as clearance
import sni.uac.token as token
import sni.uac.user as user

router = APIRouter()


class GetUserOut(pdt.BaseModel):
    """
    Model for ``GET /user/{character_name}`` requests
    """
    alliance: Optional[str]
    character_id: int
    character_name: str
    clearance_level: int
    coalitions: List[str]
    corporation: Optional[str]
    created_on: datetime
    is_ceo_of_alliance: bool
    is_ceo_of_corporation: bool
    updated_on: datetime


class PutUserIn(pdt.BaseModel):
    """
    Model for ``PUT /user/{character_name}`` requests
    """
    clearance_level: Optional[int]


def user_record_to_response(usr: user.User) -> GetUserOut:
    """
    Populates a new :class:`sni.routers.user.GetUserOut` with the information
    contained in a user database record.
    """
    corporation_name = None
    alliance_name = None
    coalition_names = []
    corporation: user.Corporation = usr.corporation
    if corporation is not None:
        corporation_name = corporation.corporation_name
        alliance: user.Alliance = corporation.alliance
        if alliance is not None:
            alliance_name = alliance.alliance_name
            coalition_names = [
                coalition.name for coalition in alliance.coalitions()
            ]
    return GetUserOut(
        alliance=alliance_name,
        character_id=usr.character_id,
        character_name=usr.character_name,
        clearance_level=usr.clearance_level,
        coalitions=coalition_names,
        corporation=corporation_name,
        created_on=usr.created_on,
        is_ceo_of_alliance=usr.is_ceo_of_alliance(),
        is_ceo_of_corporation=usr.is_ceo_of_corporation(),
        updated_on=usr.updated_on,
    )


@router.get('', response_model=List[str])
def get_user(tkn: token.Token = Depends(
    token.from_authotization_header_nondyn)):
    """
    Returns the list of all user names. Requires a clearance level of 0 or
    more.
    """
    clearance.assert_has_clearance(tkn.owner, 'sni.read_user')
    return [user.character_name for user in user.User.objects()]


@router.delete(
    '/{character_name}',
    summary='Delete a user',
)
def delete_user(character_name: str,
                tkn: token.Token = Depends(
                    token.from_authotization_header_nondyn)):
    """
    Deletes a user. Requires a clearance level of 9 or more.
    """
    clearance.assert_has_clearance(tkn.owner, 'sni.delete_user')
    usr: user.User = user.User.objects.get(character_name=character_name)
    usr.delete()


@router.get(
    '/{character_name}',
    response_model=GetUserOut,
    summary='Get basic informations about a user',
)
def get_user_name(character_name: str,
                  tkn: token.Token = Depends(
                      token.from_authotization_header_nondyn)):
    """
    Returns details about a character. Requires a clearance level of 0 or more.
    """
    clearance.assert_has_clearance(tkn.owner, 'sni.read_user')
    usr = user.User.objects.get(character_name=character_name)
    return user_record_to_response(usr)


@router.put(
    '/{character_name}',
    response_model=GetUserOut,
    summary='Update a user',
)
def put_user_name(character_name: str,
                  data: PutUserIn,
                  tkn: token.Token = Depends(
                      token.from_authotization_header_nondyn)):
    """
    Manually updates non ESI data about a character. The required clearance
    level depends on the modification.
    """
    usr: user.User = user.User.objects.get(character_name=character_name)
    if data.clearance_level is not None:
        if not 0 <= data.clearance_level <= 10:
            raise HTTPException(
                status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail=
                'Field clearance_level must be between 0 and 10 (inclusive).')
        scope_name = f'sni.set_clearance_level_{data.clearance_level}'
        clearance.assert_has_clearance(tkn.owner, scope_name, usr)
        usr.clearance_level = data.clearance_level
    usr.save()
    return user_record_to_response(usr)
