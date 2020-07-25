"""
ESI related paths
"""

from typing import Optional

from fastapi import (APIRouter, Depends, HTTPException, status)
import pydantic as pdt

from sni.user.models import User

from sni.esi.token import get_access_token
from sni.esi.esi import (
    esi_get_all_pages,
    esi_get,
    EsiResponse,
    get_esi_path_scope,
    id_annotations,
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
    all_pages: bool = False
    id_annotations: bool = False
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
            try:
                esi_token = get_access_token(
                    data.on_behalf_of,
                    esi_scope,
                ).access_token
            except LookupError:
                raise HTTPException(
                    status.HTTP_404_NOT_FOUND,
                    detail='Could not find valid ESI refresh token for ' \
                        + 'character ' + str(data.on_behalf_of),
                )

    function = esi_get_all_pages if data.all_pages else esi_get
    result = function(esi_path, esi_token, params=data.params)
    if data.id_annotations:
        result.id_annotations = id_annotations(result.data)
    return result
