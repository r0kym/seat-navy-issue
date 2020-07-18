"""
SDE (EVE Static Data Exporty) related module

See also:
    `EVE Developer Ressources <https://developers.eveonline.com/resource/resources>`_
"""

import bz2
import hashlib
import logging
import sqlite3

import requests

from .models import (
    SdeCategory,
    SdeConstellation,
    SdeGroup,
    SdeRegion,
    SdeSolarSystem,
    SdeType,
)

SDE_ROOT_URL = 'https://www.fuzzwork.co.uk/dump/'
SDE_SQLITE_MD5_URL = SDE_ROOT_URL + 'sqlite-latest.sqlite.bz2.md5'
SDE_SQLITE_DUMP_URL = SDE_ROOT_URL + 'sqlite-latest.sqlite.bz2'


def download_latest_sde(dump_path: str) -> str:
    """
    Downloads and decompresses the latest SDE sqlite dump.

    Returns:
        The MD5 checksum of the dump (before decompression).
    """
    logging.debug('Downloading and decompressing SDE Sqlite dump to %s',
                  dump_path)
    response = requests.get(SDE_SQLITE_DUMP_URL, stream=True)
    response.raise_for_status()
    decompressor = bz2.BZ2Decompressor()
    hasher = hashlib.md5()
    with open(dump_path, 'wb+') as dump:
        for data in response.iter_content(chunk_size=512):
            hasher.update(data)
            decompressed_data = decompressor.decompress(data)
            if decompressed_data:
                dump.write(decompressed_data)
    md5 = hasher.hexdigest()
    logging.debug('Downloaded latest SDE with hash %s', md5)
    return md5


def get_latest_sde_md5() -> str:
    """
    Returns the latest md5 checksum of the bz2 sqlite dump
    """
    response = requests.get(SDE_SQLITE_MD5_URL)
    response.raise_for_status()
    md5 = str(response.text).split(' ')[0]
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
    logging.debug('Importing SDE table invCategories')
    for row in client.execute('SELECT * FROM invCategories;'):
        SdeCategory.objects(category_id=row['categoryID']).update(
            set__category_id=row['categoryID'],
            set__name=row['categoryName'],
            upsert=True,
        )


def import_sde_dump_inv_groups(client: sqlite3.Connection) -> None:
    """
    Imports the ``invGroups`` table
    """
    logging.debug('Importing SDE table invGroups')
    for row in client.execute('SELECT * FROM invGroups;'):
        category = SdeCategory.objects(category_id=row['categoryID']).first()
        SdeGroup.objects(group_id=row['groupID']).update(
            set__category=category,
            set__group_id=row['groupID'],
            set__name=row['groupName'],
            upsert=True,
        )


def import_sde_dump_inv_types(client: sqlite3.Connection) -> None:
    """
    Imports the ``invTypes`` table
    """
    logging.debug('Importing SDE table invTypes')
    for row in client.execute('SELECT * FROM invTypes;'):
        group = SdeGroup.objects(group_id=row['groupID']).first()
        SdeType.objects(type_id=row['typeID']).update(
            set__group=group,
            set__name=row['typeName'],
            set__type_id=row['typeID'],
            upsert=True,
        )


def import_sde_dump_map_regions(client: sqlite3.Connection) -> None:
    """
    Imports the ``mapRegions`` table
    """
    logging.debug('Importing SDE table mapRegions')
    for row in client.execute('SELECT * FROM mapRegions;'):
        SdeRegion.objects(region_id=row['regionID']).update(
            set__region_id=row['regionID'],
            set__name=row['regionName'],
            upsert=True,
        )


def import_sde_dump_inv_constellations(client: sqlite3.Connection) -> None:
    """
    Imports the ``mapConstellations`` table
    """
    logging.debug('Importing SDE table mapConstellations')
    for row in client.execute('SELECT * FROM mapConstellations;'):
        region = SdeRegion.objects(region_id=row['regionID']).get()
        SdeConstellation.objects(
            constellation_id=row['constellationID']).update(
                set__constellation_id=row['constellationID'],
                set__name=row['constellationName'],
                set__region=region,
                upsert=True,
            )


def import_sde_dump_inv_solar_systems(client: sqlite3.Connection) -> None:
    """
    Imports the ``mapSolarSystems`` table
    """
    logging.debug('Importing SDE table mapSolarSystems')
    for row in client.execute('SELECT * FROM mapSolarSystems;'):
        constellation = SdeConstellation.objects(
            constellation_id=row['constellationID']).get()
        SdeSolarSystem.objects(solar_system_id=row['solarSystemID']).update(
            set__constellation=constellation,
            set__name=row['solarSystemName'],
            set__solar_system_id=row['solarSystemID'],
            upsert=True,
        )
