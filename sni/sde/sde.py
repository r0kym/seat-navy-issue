"""
SDE (EVE Static Data Exporty) related module

See also:
    `EVE Developer Ressources <https://developers.eveonline.com/resource/resources>`_
"""

from typing import Optional
import bz2
import hashlib
import logging
import sqlite3

import mongoengine as me
import requests

from sni.db.cache import cache_get, cache_set
from sni.utils import DAY

from .models import EsiObjectName

SDE_ROOT_URL = "https://www.fuzzwork.co.uk/dump/"
SDE_SQLITE_MD5_URL = SDE_ROOT_URL + "sqlite-latest.sqlite.bz2.md5"
SDE_SQLITE_DUMP_URL = SDE_ROOT_URL + "sqlite-latest.sqlite.bz2"


def download_latest_sde(dump_path: str) -> str:
    """
    Downloads and decompresses the latest SDE sqlite dump.

    Returns:
        The MD5 checksum of the dump (before decompression).
    """
    logging.debug(
        "Downloading and decompressing SDE Sqlite dump to %s", dump_path
    )
    response = requests.get(SDE_SQLITE_DUMP_URL, stream=True)
    response.raise_for_status()
    decompressor = bz2.BZ2Decompressor()
    hasher = hashlib.md5()  # nosec
    with open(dump_path, "wb+") as dump:
        for data in response.iter_content(chunk_size=512):
            hasher.update(data)
            decompressed_data = decompressor.decompress(data)
            if decompressed_data:
                dump.write(decompressed_data)
    md5 = hasher.hexdigest()
    logging.debug("Downloaded latest SDE with hash %s", md5)
    return md5


def get_latest_sde_md5() -> str:
    """
    Returns the latest md5 checksum of the bz2 sqlite dump
    """
    response = requests.get(SDE_SQLITE_MD5_URL)
    response.raise_for_status()
    md5 = str(response.text).split(" ")[0]
    return md5


def import_sde_dump(dump_path: str) -> None:
    """
    Imports the relevant SDE table in to the database
    """
    client = sqlite3.connect(dump_path)
    client.row_factory = sqlite3.Row
    import_sde_dump_inv_categories(client)
    import_sde_dump_inv_groups(client)
    import_sde_dump_inv_types(client)
    import_sde_dump_map_regions(client)
    import_sde_dump_inv_constellations(client)
    import_sde_dump_inv_solar_systems(client)
    client.close()


def import_sde_dump_inv_categories(client: sqlite3.Connection) -> None:
    """
    Imports the ``invCategories`` table
    """
    logging.debug("Importing SDE table invCategories")
    for row in client.execute("SELECT * FROM invCategories;"):
        EsiObjectName.objects(
            field_id=row["categoryID"], field_names="category_id",
        ).update(
            set___version=EsiObjectName.SCHEMA_VERSION,
            set__field_id=row["categoryID"],
            set__field_names=["category_id"],
            set__name=row["categoryName"],
            upsert=True,
        )


def import_sde_dump_inv_groups(client: sqlite3.Connection) -> None:
    """
    Imports the ``invGroups`` table
    """
    logging.debug("Importing SDE table invGroups")
    for row in client.execute("SELECT * FROM invGroups;"):
        EsiObjectName.objects(
            field_id=row["groupID"], field_names="group_id",
        ).update(
            set___version=EsiObjectName.SCHEMA_VERSION,
            set__field_id=row["groupID"],
            set__field_names=["group_id"],
            set__name=row["groupName"],
            upsert=True,
        )


def import_sde_dump_inv_types(client: sqlite3.Connection) -> None:
    """
    Imports the ``invTypes`` table
    """
    logging.debug("Importing SDE table invTypes")
    for row in client.execute("SELECT * FROM invTypes;"):
        EsiObjectName.objects(
            field_id=row["typeID"], field_names="type_id",
        ).update(
            set___version=EsiObjectName.SCHEMA_VERSION,
            set__field_id=row["typeID"],
            set__field_names=[
                "item_type_id",
                "ship_type_id",
                "type_id",
                "weapon_type_id",
            ],
            set__name=row["typeName"],
            upsert=True,
        )


def import_sde_dump_map_regions(client: sqlite3.Connection) -> None:
    """
    Imports the ``mapRegions`` table
    """
    logging.debug("Importing SDE table mapRegions")
    for row in client.execute("SELECT * FROM mapRegions;"):
        EsiObjectName.objects(
            field_id=row["regionID"], field_names="region_id",
        ).update(
            set___version=EsiObjectName.SCHEMA_VERSION,
            set__field_id=row["regionID"],
            set__field_names="region_id",
            set__name=row["regionName"],
            upsert=True,
        )


def import_sde_dump_inv_constellations(client: sqlite3.Connection) -> None:
    """
    Imports the ``mapConstellations`` table
    """
    logging.debug("Importing SDE table mapConstellations")
    for row in client.execute("SELECT * FROM mapConstellations;"):
        EsiObjectName.objects(
            field_id=row["constellationID"], field_names="constellation_id",
        ).update(
            set___version=EsiObjectName.SCHEMA_VERSION,
            set__field_id=row["constellationID"],
            set__field_names="constellation_id",
            set__name=row["constellationName"],
            upsert=True,
        )


def import_sde_dump_inv_solar_systems(client: sqlite3.Connection) -> None:
    """
    Imports the ``mapSolarSystems`` table
    """
    logging.debug("Importing SDE table mapSolarSystems")
    for row in client.execute("SELECT * FROM mapSolarSystems;"):
        EsiObjectName.objects(
            field_id=row["solarSystemID"], field_names="solar_system_id",
        ).update(
            set___version=EsiObjectName.SCHEMA_VERSION,
            set__field_id=row["solarSystemID"],
            set__field_names="solar_system_id",
            set__name=row["solarSystemName"],
            upsert=True,
        )


def sde_get_name(field_id: int, field_name: Optional[str]) -> Optional[str]:
    """
    Fetches a document from the ``esi_object_name`` collection. See
    :class:`sni.sde.models.EsiObjectName`.
    """
    key = ("sde:" + str(field_id), None)
    name = cache_get(key)
    if name is None:
        if field_name is None:
            query_set = EsiObjectName.objects(field_id=field_id)
        else:
            query_set = EsiObjectName.objects(
                field_id=field_id, field_names=field_name,
            )
        try:
            name = query_set.get().name
            cache_set(key, name, 1 * DAY)
        except me.DoesNotExist:
            name = None
    return name
