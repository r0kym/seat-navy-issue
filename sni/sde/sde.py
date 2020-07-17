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

from .models import SdeCategory, SdeGroup, SdeType

SDE_ROOT_URL = 'https://www.fuzzwork.co.uk/dump/'
SDE_SQLITE_MD5_URL = SDE_ROOT_URL + 'sqlite-latest.sqlite.bz2.md5'
SDE_SQLITE_DUMP_URL = SDE_ROOT_URL + 'sqlite-latest.sqlite.bz2'


def download_latest_sde(dump_path: str) -> str:
    """
    Downloads and decompresses the latest SDE sqlite dump.

    Returns:
        The MD5 checksum of the dump (before decompression).
    """
    logging.debug("Downloading and decompressing SDE Sqlite dump to %s",
                  dump_path)
    response = requests.get(SDE_SQLITE_DUMP_URL, stream=True)
    response.raise_for_status()
    decompressor = bz2.BZ2Decompressor()
    hasher = hashlib.md5()
    with open(dump_path, "wb+") as dump:
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
    sqlite_client = sqlite3.connect(dump_path)
    sqlite_client.row_factory = sqlite3.Row
    for row in sqlite_client.execute('SELECT * FROM invCategories;'):
        SdeCategory.objects(category_id=row['categoryID']).update(
            set__category_id=row['categoryID'],
            set__name=row['categoryName'],
            upsert=True,
        )
    for row in sqlite_client.execute('SELECT * FROM invGroups;'):
        category = SdeCategory.objects(category_id=row['categoryID']).first()
        SdeGroup.objects(group_id=row['groupID']).update(
            set__category=category,
            set__group_id=row['groupID'],
            set__name=row['groupName'],
            upsert=True,
        )
    for row in sqlite_client.execute('SELECT * FROM invTypes;'):
        group = SdeGroup.objects(group_id=row['groupID']).first()
        SdeType.objects(type_id=row['typeID']).update(
            set__group=group,
            set__name=row['typeName'],
            set__type_id=row['typeID'],
            upsert=True,
        )
    sqlite_client.close()
