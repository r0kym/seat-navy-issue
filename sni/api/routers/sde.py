"""
SDE paths
"""

from typing import Dict, List, Optional

from fastapi import APIRouter, Depends
import pydantic as pdt

from sni.uac.token import (
    from_authotization_header_nondyn,
    Token,
)

from sni.sde.models import SdeType

router = APIRouter()


class GetSdeTypeOut(pdt.BaseModel):
    """
    Represents an SDE type
    """
    category_name: Optional[str]
    group_name: Optional[str]
    type_name: Optional[str]


def sde_type_record_to_response(record: SdeType) -> GetSdeTypeOut:
    """
    Converts an instance of :class:`sni.sde.models.SdeType` to :class:`sni.api.routers.sde.GetSdeTypeOut`
    """
    return GetSdeTypeOut(
        category_name=record.category_name,
        group_name=record.group_name,
        type_name=record.name,
    )


@router.get(
    '/type',
    response_model=Dict[int, Optional[GetSdeTypeOut]],
    summary='Get information about a list of SDE types',
)
def get_sde_types(
        data: List[int],
        _tkn: Token = Depends(from_authotization_header_nondyn),
):
    """
    Given a list of SDE type ids, returns a dict with informations about these
    types. The return dict key set is guaranteed to be the same as the input
    list (up to repetition of keys).

    This method does not check the token.

    Example:
        Sending a request with ``[21554, 1, 19722]`` returns::

            {
                "1": null,
                "21554": {
                    "category_name": "Blueprint",
                    "group_name": "Projectile Weapon Blueprint",
                    "type_name": "650mm Medium 'Jolt' Artillery I Blueprint"
                },
                "19722": {
                    "category_name": "Ship",
                    "group_name": "Dreadnought",
                    "type_name": "Naglfar"
                }
            }
    """
    result: Dict[int, Optional[GetSdeTypeOut]] = {}
    for type_id in set(data):
        type_record = SdeType.objects(type_id=type_id).first()
        if type_record is None:
            result[type_id] = None
        else:
            result[type_id] = sde_type_record_to_response(type_record)
    return result
