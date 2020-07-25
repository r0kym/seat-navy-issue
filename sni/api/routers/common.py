"""
Stuff that is common to all routers
"""

from typing import Any

from bson.objectid import ObjectId


class BSONObjectId(ObjectId):
    """
    A pydantic-compatible BSON ObjectId
    """
    @classmethod
    def __get_validators__(cls):
        """
        See `pydantic Custom Data Types <https://pydantic-docs.helpmanual.io/usage/types/#custom-data-types>`_
        """
        yield cls.validate

    @classmethod
    def __modify_schema__(cls, field_schema: dict) -> None:
        """
        See `pydantic Custom Data Types <https://pydantic-docs.helpmanual.io/usage/types/#custom-data-types>`_
        """
        field_schema.update(
            title='BSON object id',
            examples=['ObjectId(\'5f0835370ad0d76f0647713c\')'],
        )

    @classmethod
    def validate(cls, value: Any) -> 'BSONObjectId':
        """
        Validates the value. yep
        """
        if not isinstance(value, (ObjectId, str)):
            raise TypeError('ObjectId or string required')
        try:
            return ObjectId(value)
        except:
            raise ValueError('invalid BSON object id')
