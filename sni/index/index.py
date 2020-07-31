"""
Main indexation module. Allows searches and analytics over data pulled from the
ESI.
"""

from sni.esi.token import esi_get_on_befalf_of
from sni.user.models import User

from .models import EsiCharacterLocation


def get_user_location(
    usr: User, invalidate_token_on_error: bool = False
) -> EsiCharacterLocation:
    """
    Get a character's current location
    """
    location_data = esi_get_on_befalf_of(
        f"latest/characters/{usr.character_id}/location/",
        usr.character_id,
        invalidate_token_on_error=invalidate_token_on_error,
        raise_for_status=True,
    ).data
    online_data = esi_get_on_befalf_of(
        f"latest/characters/{usr.character_id}/online/",
        usr.character_id,
        invalidate_token_on_error=invalidate_token_on_error,
        raise_for_status=True,
    ).data
    ship_data = esi_get_on_befalf_of(
        f"latest/characters/{usr.character_id}/ship/",
        usr.character_id,
        invalidate_token_on_error=invalidate_token_on_error,
        raise_for_status=True,
    ).data
    return EsiCharacterLocation(
        online=online_data["online"],
        ship_item_id=ship_data["ship_item_id"],
        ship_name=ship_data["ship_name"],
        ship_type_id=ship_data["ship_type_id"],
        solar_system_id=location_data["solar_system_id"],
        station_id=location_data.get("station_id"),
        structure_id=location_data.get("structure_id"),
        user=usr,
    )
