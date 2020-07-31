"""
EVE ESI (public API) layer
"""

from enum import Enum
from typing import Any, Dict, Optional
import logging
import re

from dateutil import parser
import mongoengine as me
import pydantic as pdt
from requests import request, Response

from sni.db.cache import cache_get, cache_set
from sni.sde.sde import sde_get_name
from sni.conf import CONFIGURATION as conf
import sni.utils as utils

from .models import EsiPath

ESI_BASE = "https://esi.evetech.net/"
ESI_SWAGGER = ESI_BASE + "latest/swagger.json"


class EsiResponse(pdt.BaseModel):
    """
    A model for ESI responses
    """

    data: Any
    headers: dict = {}
    id_annotations: dict = {}
    status_code: int

    @staticmethod
    def from_response(response: Response) -> "EsiResponse":
        """
        Converts a :class:`request.Response` object to a
        :class:`sni.esi.esi.EsiResponse`.
        """
        return EsiResponse(
            data=response.json(),
            headers=dict(response.headers),
            status_code=response.status_code,
        )


class EsiScope(str, Enum):
    """
    Enumeration of the ESI scopes
    """

    ESI_ALLIANCES_READ_CONTACTS_V1 = "esi-alliances.read_contacts.v1"
    ESI_ASSETS_READ_ASSETS_V1 = "esi-assets.read_assets.v1"
    ESI_ASSETS_READ_CORPORATION_ASSETS_V1 = (
        "esi-assets.read_corporation_assets.v1"
    )
    ESI_BOOKMARKS_READ_CHARACTER_BOOKMARKS_V1 = (
        "esi-bookmarks.read_character_bookmarks.v1"
    )
    ESI_BOOKMARKS_READ_CORPORATION_BOOKMARKS_V1 = (
        "esi-bookmarks.read_corporation_bookmarks.v1"
    )
    ESI_CALENDAR_READ_CALENDAR_EVENTS_V1 = (
        "esi-calendar.read_calendar_events.v1"
    )
    ESI_CALENDAR_RESPOND_CALENDAR_EVENTS_V1 = (
        "esi-calendar.respond_calendar_events.v1"
    )
    ESI_CHARACTERS_READ_AGENTS_RESEARCH_V1 = (
        "esi-characters.read_agents_research.v1"
    )
    ESI_CHARACTERS_READ_BLUEPRINTS_V1 = "esi-characters.read_blueprints.v1"
    ESI_CHARACTERS_READ_CHAT_CHANNELS_V1 = (
        "esi-characters.read_chat_channels.v1"
    )
    ESI_CHARACTERS_READ_CONTACTS_V1 = "esi-characters.read_contacts.v1"
    ESI_CHARACTERS_READ_CORPORATION_ROLES_V1 = (
        "esi-characters.read_corporation_roles.v1"
    )
    ESI_CHARACTERS_READ_FATIGUE_V1 = "esi-characters.read_fatigue.v1"
    ESI_CHARACTERS_READ_FW_STATS_V1 = "esi-characters.read_fw_stats.v1"
    ESI_CHARACTERS_READ_LOYALTY_V1 = "esi-characters.read_loyalty.v1"
    ESI_CHARACTERS_READ_MEDALS_V1 = "esi-characters.read_medals.v1"
    ESI_CHARACTERS_READ_NOTIFICATIONS_V1 = (
        "esi-characters.read_notifications.v1"
    )
    ESI_CHARACTERS_READ_OPPORTUNITIES_V1 = (
        "esi-characters.read_opportunities.v1"
    )
    ESI_CHARACTERS_READ_STANDINGS_V1 = "esi-characters.read_standings.v1"
    ESI_CHARACTERS_READ_TITLES_V1 = "esi-characters.read_titles.v1"
    ESI_CHARACTERS_WRITE_CONTACTS_V1 = "esi-characters.write_contacts.v1"
    ESI_CHARACTERSTATS_READ_V1 = "esi-characterstats.read.v1"
    ESI_CLONES_READ_CLONES_V1 = "esi-clones.read_clones.v1"
    ESI_CLONES_READ_IMPLANTS_V1 = "esi-clones.read_implants.v1"
    ESI_CONTRACTS_READ_CHARACTER_CONTRACTS_V1 = (
        "esi-contracts.read_character_contracts.v1"
    )
    ESI_CONTRACTS_READ_CORPORATION_CONTRACTS_V1 = (
        "esi-contracts.read_corporation_contracts.v1"
    )
    ESI_CORPORATIONS_READ_BLUEPRINTS_V1 = "esi-corporations.read_blueprints.v1"
    ESI_CORPORATIONS_READ_CONTACTS_V1 = "esi-corporations.read_contacts.v1"
    ESI_CORPORATIONS_READ_CONTAINER_LOGS_V1 = (
        "esi-corporations.read_container_logs.v1"
    )
    ESI_CORPORATIONS_READ_CORPORATION_MEMBERSHIP_V1 = (
        "esi-corporations.read_corporation_membership.v1"
    )
    ESI_CORPORATIONS_READ_DIVISIONS_V1 = "esi-corporations.read_divisions.v1"
    ESI_CORPORATIONS_READ_FACILITIES_V1 = "esi-corporations.read_facilities.v1"
    ESI_CORPORATIONS_READ_FW_STATS_V1 = "esi-corporations.read_fw_stats.v1"
    ESI_CORPORATIONS_READ_MEDALS_V1 = "esi-corporations.read_medals.v1"
    ESI_CORPORATIONS_READ_STANDINGS_V1 = "esi-corporations.read_standings.v1"
    ESI_CORPORATIONS_READ_STARBASES_V1 = "esi-corporations.read_starbases.v1"
    ESI_CORPORATIONS_READ_STRUCTURES_V1 = "esi-corporations.read_structures.v1"
    ESI_CORPORATIONS_READ_TITLES_V1 = "esi-corporations.read_titles.v1"
    ESI_CORPORATIONS_TRACK_MEMBERS_V1 = "esi-corporations.track_members.v1"
    ESI_FITTINGS_READ_FITTINGS_V1 = "esi-fittings.read_fittings.v1"
    ESI_FITTINGS_WRITE_FITTINGS_V1 = "esi-fittings.write_fittings.v1"
    ESI_FLEETS_READ_FLEET_V1 = "esi-fleets.read_fleet.v1"
    ESI_FLEETS_WRITE_FLEET_V1 = "esi-fleets.write_fleet.v1"
    ESI_INDUSTRY_READ_CHARACTER_JOBS_V1 = "esi-industry.read_character_jobs.v1"
    ESI_INDUSTRY_READ_CHARACTER_MINING_V1 = (
        "esi-industry.read_character_mining.v1"
    )
    ESI_INDUSTRY_READ_CORPORATION_JOBS_V1 = (
        "esi-industry.read_corporation_jobs.v1"
    )
    ESI_INDUSTRY_READ_CORPORATION_MINING_V1 = (
        "esi-industry.read_corporation_mining.v1"
    )
    ESI_KILLMAILS_READ_CORPORATION_KILLMAILS_V1 = (
        "esi-killmails.read_corporation_killmails.v1"
    )
    ESI_KILLMAILS_READ_KILLMAILS_V1 = "esi-killmails.read_killmails.v1"
    ESI_LOCATION_READ_LOCATION_V1 = "esi-location.read_location.v1"
    ESI_LOCATION_READ_ONLINE_V1 = "esi-location.read_online.v1"
    ESI_LOCATION_READ_SHIP_TYPE_V1 = "esi-location.read_ship_type.v1"
    ESI_MAIL_ORGANIZE_MAIL_V1 = "esi-mail.organize_mail.v1"
    ESI_MAIL_READ_MAIL_V1 = "esi-mail.read_mail.v1"
    ESI_MAIL_SEND_MAIL_V1 = "esi-mail.send_mail.v1"
    ESI_MARKETS_READ_CHARACTER_ORDERS_V1 = (
        "esi-markets.read_character_orders.v1"
    )
    ESI_MARKETS_READ_CORPORATION_ORDERS_V1 = (
        "esi-markets.read_corporation_orders.v1"
    )
    ESI_MARKETS_STRUCTURE_MARKETS_V1 = "esi-markets.structure_markets.v1"
    ESI_PLANETS_MANAGE_PLANETS_V1 = "esi-planets.manage_planets.v1"
    ESI_PLANETS_READ_CUSTOMS_OFFICES_V1 = "esi-planets.read_customs_offices.v1"
    ESI_SEARCH_SEARCH_STRUCTURES_V1 = "esi-search.search_structures.v1"
    ESI_SKILLS_READ_SKILLQUEUE_V1 = "esi-skills.read_skillqueue.v1"
    ESI_SKILLS_READ_SKILLS_V1 = "esi-skills.read_skills.v1"
    ESI_UI_OPEN_WINDOW_V1 = "esi-ui.open_window.v1"
    ESI_UI_WRITE_WAYPOINT_V1 = "esi-ui.write_waypoint.v1"
    ESI_UNIVERSE_READ_STRUCTURES_V1 = "esi-universe.read_structures.v1"
    ESI_WALLET_READ_CHARACTER_WALLET_V1 = "esi-wallet.read_character_wallet.v1"
    ESI_WALLET_READ_CORPORATION_WALLET_V1 = (
        "esi-wallet.read_corporation_wallet.v1"
    )
    ESI_WALLET_READ_CORPORATION_WALLETS_V1 = (
        "esi-wallet.read_corporation_wallets.v1"
    )
    PUBLICDATA = "publicData"


# pylint: disable=dangerous-default-value
def esi_delete(
    path: str, *, kwargs: dict = {}, token: Optional[str] = None,
) -> EsiResponse:
    """
    Wrapper for :meth:`sni.esi.esi.esi_request` for DELETE requests.
    """
    return esi_request("delete", path, token=token, kwargs=kwargs)


# pylint: disable=dangerous-default-value
def esi_get(
    path: str, *, kwargs: dict = {}, token: Optional[str] = None,
) -> EsiResponse:
    """
    Wrapper for :meth:`sni.esi.esi.esi_request` for GET requests.
    """
    return esi_request("get", path, token=token, kwargs=kwargs)


# pylint: disable=dangerous-default-value
def esi_get_all_pages(
    path: str, *, token: Optional[str] = None, kwargs: dict = {},
) -> EsiResponse:
    """
    Returns all pages of an ESI GET path
    """
    current_page = 1
    max_page = 1
    response_data = []
    response_headers = {}
    response_status_code = -1
    if "params" not in kwargs:
        kwargs["params"] = {}
    while current_page <= max_page:
        kwargs["params"]["page"] = current_page
        current_response = esi_request("get", path, token=token, kwargs=kwargs)
        response_data += current_response.data
        response_headers = current_response.headers
        response_status_code = current_response.status_code
        max_page = int(current_response.headers.get("X-Pages", -1))
        current_page += 1
    return EsiResponse(
        data=response_data,
        headers=response_headers,
        status_code=response_status_code,
    )


# pylint: disable=dangerous-default-value
def esi_post(
    path: str, *, kwargs: dict = {}, token: Optional[str] = None,
) -> EsiResponse:
    """
    Wrapper for :meth:`sni.esi.esi.esi_request` for POST requests.
    """
    return esi_request("post", path, token=token, kwargs=kwargs)


# pylint: disable=dangerous-default-value
def esi_put(
    path: str, *, kwargs: dict = {}, token: Optional[str] = None,
) -> EsiResponse:
    """
    Wrapper for :meth:`sni.esi.esi.esi_request` for PUT requests.
    """
    return esi_request("put", path, token=token, kwargs=kwargs)


# pylint: disable=dangerous-default-value
def esi_request(
    http_method: str,
    path: str,
    *,
    kwargs: dict = {},
    raise_for_status: bool = False,
    token: Optional[str] = None,
) -> EsiResponse:
    """
    Makes an HTTP request to the ESI, and returns the response object.
    """
    kwargs["headers"] = {
        "Accept-Encoding": "gzip",
        "accept": "application/json",
        "User-Agent": "SeAT Navy Issue @ " + conf.general.root_url,
        **kwargs.get("headers", {}),
    }
    if token:
        kwargs["headers"]["Authorization"] = "Bearer " + token

    if http_method.upper() != "GET":
        raw = request(http_method, ESI_BASE + path, **kwargs)
        if raise_for_status:
            raw.raise_for_status()
        return EsiResponse.from_response(raw)

    key = [path, token, kwargs.get("params")]
    response = cache_get(key)
    if response is not None:
        return EsiResponse(**response)

    raw = request(http_method, ESI_BASE + path, **kwargs)
    if raise_for_status:
        raw.raise_for_status()
    response = EsiResponse.from_response(raw)

    if not 400 <= response.status_code <= 599:
        ttl = 60
        if "Expires" in response.headers:
            try:
                ttl = int(
                    (
                        parser.parse(response.headers["Expires"]) - utils.now()
                    ).total_seconds()
                )
            except ValueError as error:
                logging.warning("Could not determine ESI TTL: %s", str(error))
        if ttl > 0:
            cache_set(key, response.dict(), ttl)

    return response


def get_esi_path_scope(path: str) -> Optional[str]:
    """
    Returns the ESI scope that is required for a given ESI path.

    Raises :class:`mongoengine.DoesNotExist` if no suitable path is found.

    Examples:

        >>> get_esi_path_scope('latest/characters/0000000000/assets')
        'esi-assets.read_assets.v1'

        >>> get_esi_path_scope('latest/alliances')
        None
    """
    esi_path: EsiPath
    for esi_path in EsiPath.objects:
        # print(esi_path.to_json())
        if re.search(esi_path.path_re, path):
            return esi_path.scope
    raise me.DoesNotExist


def id_annotations(data: Any) -> Dict[int, str]:
    """
    Annotates a JSON document. In documents returned by the ESI, ID fields
    always have the same name (e.g. `solar_system_id`, `character_id`, etc.).
    This method recursively searches for these ID fields and returns a dict
    mapping these IDs to a name.
    """
    annotations: Dict[int, str] = {}
    if isinstance(data, dict):
        for key, val in data.items():
            if key.endswith("_id") and isinstance(val, int):
                name = id_to_name(val, key)
                if name:
                    annotations[val] = name
            else:
                annotations.update(id_annotations(val))
    elif isinstance(data, list):
        for element in data:
            annotations.update(id_annotations(element))
    return annotations


def id_to_name(id_field_value: int, id_field_name: str) -> str:
    """
    Converts an object ID (e.g. station, solar system, SDE type) to a name.
    """
    annotators = {
        "alliance_id": ("latest/alliances/{}/", "name"),
        "asteroid_belt_id": ("latest/universe/asteroid_belts/{}/", "name"),
        "character_id": ("latest/characters/{}/", "name"),
        "corporation_id": ("latest/corporations/{}/", "name"),
        "graphic_id": ("latest/universe/graphics/{}/", "graphic_file"),
        "moon_id": ("latest/universe/moons/{}/", "name"),
        "planet_id": ("latest/universe/planets/{}/", "name"),
        "star_id": ("latest/universe/stars/{}/", "name"),
        "stargate_id": ("latest/universe/stargates/{}/", "name"),
        "station_id": ("latest/universe/stations/{}/", "name"),
        "structure_id": ("latest/universe/structures/{}/", "name"),
    }
    if id_field_name in annotators:
        annotator = annotators[id_field_name]
        raw = esi_get(annotator[0].format(id_field_value))
        result = raw.data.get(annotator[1])
    else:
        result = sde_get_name(id_field_value, id_field_name)
    return result if result is not None else ""


def load_esi_openapi() -> None:
    """
    Loads the ESI Swagger API into the database.

    Should be called in the initialization stage.

    See also:
        :class:`sni.esi.esi.EsiPath`
        `EVE Swagger Interface <https://esi.evetech.net/ui>`_
        `EVE Swagger Interface (JSON) <https://esi.evetech.net/latest/swagger.json>`_
    """
    logging.info("Loading ESI swagger specifications %s", ESI_SWAGGER)
    swagger = request("GET", ESI_SWAGGER).json()
    base_path = swagger["basePath"][1:]
    for path, path_data in swagger["paths"].items():
        for method, method_data in path_data.items():
            full_path = base_path + path
            path_re = "^" + re.sub(r"{\w+_id}", "[^/]+", full_path) + "?$"
            scope = None
            for security in method_data.get("security", []):
                scope = security.get("evesso", [scope])[0]
            EsiPath.objects(http_method=method, path=full_path,).update(
                set__http_method=method,
                set__path_re=path_re,
                set__path=full_path,
                set__scope=scope,
                set__version="latest",
                upsert=True,
            )
