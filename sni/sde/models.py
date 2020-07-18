"""
Teamspeak database models
"""

from typing import Optional

import mongoengine as me


class SdeCategory(me.Document):
    """
    Represents an SDE category, i.e. an entry in the ``invCategories`` table.
    """

    name = me.StringField(null=True)
    """SDE ``categoryName``"""

    category_id = me.IntField(unique=True)
    """SDE ``categoryID``"""

    meta = {
        'indexes': [
            'category_id',
        ],
    }


class SdeGroup(me.Document):
    """
    Represents an SDE category, i.e. an entry in the ``invCategories`` table.
    """

    category = me.ReferenceField(SdeCategory, null=True)
    """Reference to the associated category (``categoryID`` field)"""

    name = me.StringField(null=True)
    """SDE ``groupName``"""

    group_id = me.IntField(unique=True)
    """SDE ``groupID``"""

    meta = {
        'indexes': [
            'group_id',
        ],
    }

    @property
    def category_name(self) -> Optional[str]:
        """
        Returns the group name of this type, or ``None`` if the group does not
        have any category
        """
        return self.category.name if self.category is not None else None


class SdeType(me.Document):
    """
    Represents an SDE type, i.e. an entry in the ``invTypes`` table.
    """

    name = me.StringField(null=True)
    """SDE ``typeName``"""

    group = me.ReferenceField(SdeGroup, null=True)
    """Reference to the associated group (``groupID`` field)"""

    type_id = me.IntField(unique=True)
    """SDE ``typeID``"""

    meta = {
        'indexes': [
            'type_id',
        ],
    }

    @property
    def category_name(self) -> Optional[str]:
        """
        Returns the group name of this type, or ``None`` if the type does not
        have any group
        """
        return self.group.category_name if self.group is not None else None

    @property
    def group_name(self) -> Optional[str]:
        """
        Returns the group name of this type, or ``None`` if the type does not
        have any group
        """
        return self.group.name if self.group is not None else None


class SdeRegion(me.Document):
    """
    Represents a region in EVE, i.e. an entry in the ``mapRegions`` table.
    """

    name = me.StringField()
    """Region name (``regionName`` field)"""

    region_id = me.IntField(unique=True)
    """Region ID (``regionID`` field)"""

    meta = {
        'indexes': [
            'region_id',
        ],
    }


class SdeConstellation(me.Document):
    """
    Represents a constellation in EVE, i.e. an entry in the
    ``mapConstellations`` table.
    """

    constellation_id = me.IntField(unique=True)
    """Region ID (``constellationID`` field)"""

    name = me.StringField()
    """Region name (``constellationName`` field)"""

    region = me.ReferenceField(SdeRegion)
    """Region of this constellation"""

    meta = {
        'indexes': [
            'constellation_id',
        ],
    }

    @property
    def region_name(self) -> str:
        """
        Convenience function that returns the name of the region of this
        constellation
        """
        return self.region.name


class SdeSolarSystem(me.Document):
    """
    Represents a constellation in EVE, i.e. an entry in the
    ``mapSolarSystems`` table.
    """

    constellation = me.ReferenceField(SdeConstellation)
    """Constellation of this solar system"""

    name = me.StringField()
    """Solar system name (``solarSystemName`` field)"""

    solar_system_id = me.IntField(unique=True)
    """Solar system ID (``solarSystemID`` field)"""

    meta = {
        'indexes': [
            'solar_system_id',
        ],
    }

    @property
    def constellation_name(self) -> str:
        """
        Convenience function that returns the name of the constellation of this
        solar system
        """
        return self.constellation.name

    @property
    def region_name(self) -> str:
        """
        Convenience function that returns the name of the region of this solar
        system
        """
        return self.constellation.region_name
