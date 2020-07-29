"""
Stuff that is common to all routers
"""

from math import ceil
from typing import Any

from bson.objectid import ObjectId
from fastapi import HTTPException, Response, status
from mongoengine import QuerySet


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
            title="BSON object id",
            examples=["ObjectId('5f0835370ad0d76f0647713c')"],
        )

    @classmethod
    def validate(cls, value: Any) -> "BSONObjectId":
        """
        Validates the value. yep
        """
        if not isinstance(value, (ObjectId, str)):
            raise TypeError("ObjectId or string required")
        try:
            return ObjectId(value)
        except:
            raise ValueError("invalid BSON object id")


def paginate(
    query_set: QuerySet, page_size: int, page_index: int, response: Response,
) -> QuerySet:
    """
    Paginates a query set, sets the ``X-Pages`` header in the response. Raises
    a 422 if the page index is invalid.
    """
    max_page = ceil(query_set.count() / page_size)
    if not 1 <= page_index <= max_page:
        raise HTTPException(
            detail="Invalid page index",
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        )
    response.headers["X-Pages"] = str(max_page)
    return query_set[(page_index - 1) * page_size : page_index * page_size]
