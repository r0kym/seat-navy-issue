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

from sni.sde.models import (
    SdeCategory,
    SdeConstellation,
    SdeGroup,
    SdeRegion,
    SdeSolarSystem,
    SdeType,
)

router = APIRouter()


class GetSdeCategoryOut(pdt.BaseModel):
    """
    Represents an SDE category
    """
    category_name: Optional[str]


class GetSdeGroupOut(pdt.BaseModel):
    """
    Represents an SDE group
    """
    category_name: Optional[str]
    group_name: Optional[str]


class GetSdeTypeOut(pdt.BaseModel):
    """
    Represents an SDE type
    """
    category_name: Optional[str]
    group_name: Optional[str]
    type_name: Optional[str]


class GetSdeRegionOut(pdt.BaseModel):
    """
    Represents an SDE EVE region
    """
    region_name: str

    @staticmethod
    def from_record(record: SdeRegion) -> 'GetSdeRegionOut':
        """
        Converts an instance of :class:`sni.sde.models.SdeRegion` to
        :class:`sni.api.routers.sde.GetSdeRegionOut`
        """
        return GetSdeRegionOut(region_name=record.name)


class GetSdeConstellationOut(pdt.BaseModel):
    """
    Represents an SDE EVE constellation
    """
    constellation_name: str
    region_name: str

    @staticmethod
    def from_record(record: SdeConstellation) -> 'GetSdeConstellationOut':
        """
        Converts an instance of :class:`sni.sde.models.SdeConstellation` to
        :class:`sni.api.routers.sde.GetSdeConstellationOut`
        """
        return GetSdeConstellationOut(
            constellation_name=record.name,
            region_name=record.region_name,
        )


class GetSdeSolarSystemOut(pdt.BaseModel):
    """
    Represents an SDE EVE solar system
    """
    constellation_name: str
    region_name: str
    solar_system_name: str

    @staticmethod
    def from_record(record: SdeSolarSystem) -> 'GetSdeSolarSystemOut':
        """
        Converts an instance of :class:`sni.sde.models.SdeSolarSystem` to
        :class:`sni.api.routers.sde.GetSdeSolarSystemOut`
        """
        return GetSdeSolarSystemOut(
            constellation_name=record.constellation_name,
            region_name=record.region_name,
            solar_system_name=record.name,
        )


def sde_category_record_to_response(record: SdeCategory) -> GetSdeCategoryOut:
    """
    Converts an instance of :class:`sni.sde.models.SdeCategory` to :class:`sni.api.routers.sde.GetSdeCategoryOut`
    """
    return GetSdeCategoryOut(category_name=record.name)


def sde_group_record_to_response(record: SdeGroup) -> GetSdeGroupOut:
    """
    Converts an instance of :class:`sni.sde.models.SdeType` to :class:`sni.api.routers.sde.GetSdeTypeOut`
    """
    return GetSdeGroupOut(
        category_name=record.category_name,
        group_name=record.name,
    )


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
    '/category',
    response_model=Dict[int, Optional[GetSdeCategoryOut]],
    summary='Get information about a list of SDE categories',
)
def get_sde_category(
        data: List[int],
        _tkn: Token = Depends(from_authotization_header_nondyn),
):
    """
    Given a list of SDE category ids, returns a dict with informations about
    these types. The return dict key set is guaranteed to be the same as the
    input list (up to repetition of keys).

    Example: Sending a request with ``[-1, 7, 8, 9]`` returns::

        {
            "8": {
                "category_name": "Charge"
            },
            "9": {
                "category_name": "Blueprint"
            },
            "-1": null,
            "7": {
                "category_name": "Module"
            }
        }

    """
    result: Dict[int, Optional[GetSdeCategoryOut]] = {}
    for category_id in set(data):
        record = SdeCategory.objects(category_id=category_id).first()
        if record is None:
            result[category_id] = None
        else:
            result[category_id] = sde_category_record_to_response(record)
    return result


@router.get(
    '/group',
    response_model=Dict[int, Optional[GetSdeGroupOut]],
    summary='Get information about a list of SDE groups',
)
def get_sde_group(
        data: List[int],
        _tkn: Token = Depends(from_authotization_header_nondyn),
):
    """
    Given a list of SDE group ids, returns a dict with informations about these
    types. The return dict key set is guaranteed to be the same as the input
    list (up to repetition of keys).

    Example: Sending a request with ``[-1, 4060, 646]`` returns::

        {
            "646": {
                "category_name": "Module",
                "group_name": "Drone Tracking Modules"
            },
            "4060": {
                "category_name": "Module",
                "group_name": "Vorton Projector"
            },
            "-1": null
        }

    """
    result: Dict[int, Optional[GetSdeGroupOut]] = {}
    for group_id in set(data):
        record = SdeGroup.objects(group_id=group_id).first()
        if record is None:
            result[group_id] = None
        else:
            result[group_id] = sde_group_record_to_response(record)
    return result


@router.get(
    '/type',
    response_model=Dict[int, Optional[GetSdeTypeOut]],
    summary='Get information about a list of SDE types',
)
def get_sde_type(
        data: List[int],
        _tkn: Token = Depends(from_authotization_header_nondyn),
):
    """
    Given a list of SDE type ids, returns a dict with informations about these
    types. The return dict key set is guaranteed to be the same as the input
    list (up to repetition of keys).

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
        record = SdeType.objects(type_id=type_id).first()
        if record is None:
            result[type_id] = None
        else:
            result[type_id] = sde_type_record_to_response(record)
    return result


@router.get(
    '/region',
    response_model=Dict[int, Optional[GetSdeRegionOut]],
    summary='Get information about a list of EVE regions',
)
def get_sde_region(
        data: List[int],
        _tkn: Token = Depends(from_authotization_header_nondyn),
):
    """
    Given a list of SDE region ids, returns a dict with informations about
    these types. The return dict key set is guaranteed to be the same as the
    input list (up to repetition of keys).

    Example:
        Sending a request with ``[1, 10000060, 10000065]`` returns::

            {
                "1": null,
                "10000065": {
                    "region_name": "Kor-Azor"
                },
                "10000060": {
                    "region_name": "Delve"
                }
            }

    """
    result: Dict[int, Optional[GetSdeRegionOut]] = {}
    for region_id in set(data):
        record = SdeRegion.objects(region_id=region_id).first()
        if record is None:
            result[region_id] = None
        else:
            result[region_id] = GetSdeRegionOut.from_record(record)
    return result


@router.get(
    '/constellation',
    response_model=Dict[int, Optional[GetSdeConstellationOut]],
    summary='Get information about a list of EVE constellations',
)
def get_sde_constellation(
        data: List[int],
        _tkn: Token = Depends(from_authotization_header_nondyn),
):
    """
    Given a list of SDE constellation ids, returns a dict with informations
    about these types. The return dict key set is guaranteed to be the same as
    the input list (up to repetition of keys).

    Example:
        Sending a request with ``[1, 20000352, 20000681]`` returns::

            {
                "20000352": {
                    "constellation_name": "Besateoden",
                    "region_name": "Molden Heath"
                },
                "1": null,
                "20000681": {
                    "constellation_name": "Basilisk",
                    "region_name": "Fountain"
                }
            }

    """
    result: Dict[int, Optional[GetSdeConstellationOut]] = {}
    for constellation_id in set(data):
        record = SdeConstellation.objects(
            constellation_id=constellation_id).first()
        if record is None:
            result[constellation_id] = None
        else:
            result[constellation_id] = GetSdeConstellationOut.from_record(
                record)
    return result


@router.get(
    '/solar_system',
    response_model=Dict[int, Optional[GetSdeSolarSystemOut]],
    summary='Get information about a list of EVE solar systems',
)
def get_sde_solar_system(
        data: List[int],
        _tkn: Token = Depends(from_authotization_header_nondyn),
):
    """
    Given a list of SDE solar system ids, returns a dict with informations
    about these types. The return dict key set is guaranteed to be the same as
    the input list (up to repetition of keys).

    Example:
        Sending a request with ``[1, 30003878, 31001039]`` returns::

            {
                "1": null,
                "30003878": {
                    "constellation_name": "Amdimmah",
                    "region_name": "Khanid",
                    "solar_system_name": "Palas"
                },
                "31001039": {
                    "constellation_name": "C-C00100",
                    "region_name": "C-R00011",
                    "solar_system_name": "J171549"
                }
            }

    """
    result: Dict[int, Optional[GetSdeSolarSystemOut]] = {}
    for solar_system_id in set(data):
        record = SdeSolarSystem.objects(
            solar_system_id=solar_system_id).first()
        if record is None:
            result[solar_system_id] = None
        else:
            result[solar_system_id] = GetSdeSolarSystemOut.from_record(record)
    return result
