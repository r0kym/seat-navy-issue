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
