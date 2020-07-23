"""
ESI related paths
"""

from typing import Optional

from fastapi import APIRouter, Depends
import pydantic as pdt

from sni.user.models import User

from sni.esi.token import get_access_token
from sni.esi.esi import (
    esi_get,
    EsiResponse,
    get_esi_path_scope,
)
from sni.uac.clearance import assert_has_clearance
from sni.uac.token import (
    from_authotization_header_nondyn,
    Token,
)

router = APIRouter()


class EsiRequestIn(pdt.BaseModel):
    """
    Data to be forwarded to the ESI
    """
    on_behalf_of: Optional[int] = None
    params: dict = {}


@router.get(
    '/{esi_path:path}',
    response_model=EsiResponse,
    summary='Proxy path to the ESI',
    tags=['ESI'],
)
async def get_esi_latest(
        esi_path: str,
        data: EsiRequestIn = EsiRequestIn(),
        tkn: Token = Depends(from_authotization_header_nondyn),
):
    """
    Forwards a `GET` request to the ESI. The required clearance level depends
    on the user making the request and the user specified on the
    `on_behalf_of` field. See also `EsiRequestIn`.
    """
    esi_token: Optional[str] = None
    if data.on_behalf_of:
        esi_scope = get_esi_path_scope(esi_path)
        if esi_scope is not None:
            target = User.objects.get(character_id=data.on_behalf_of)
            assert_has_clearance(tkn.owner, esi_scope, target)
            esi_token = get_access_token(
                data.on_behalf_of,
                esi_scope,
            ).access_token
    return esi_get(esi_path, esi_token, params=data.params)
