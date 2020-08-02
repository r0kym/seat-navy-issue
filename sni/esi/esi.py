"""
EVE ESI (public API) layer
"""

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

from .models import EsiPath, EsiScope

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


def get_esi_path_scope(path: str) -> Optional[EsiScope]:
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
