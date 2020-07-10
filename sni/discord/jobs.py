"""
Discord jobs.

These jobs run on a dedicated asyncio scheduler.
"""

from discord import Member

import sni.utils as utils
from sni.user.models import Group, User

from .bot import (
    get_guild,
    get_member,
    scheduler,
)


async def map_discord_roles():
    """
    Ensure that roles corresponding to SNI groups (whose ``map_to_discord`` is
    ``True``) exist
    """
    guild = get_guild()
    current_roles = {role.name: role for role in guild.roles}
    for grp in Group.objects(map_to_discord=True):
        if grp.group_name in current_roles.keys():
            grp.discord_role_id = current_roles[grp.group_name].id
        else:
            role = await guild.create_role(name=grp.group_name)
            grp.discord_role_id = role.id
        grp.save()


async def update_discord_user(usr: User):
    """
    Updates a discord user. Doesn't modify their roles.
    """
    member: Member = get_member(usr.discord_user_id)
    await member.edit(
        nick=usr.tickered_name,
        reason='SeAT Navy Issue',
    )


@scheduler.scheduled_job('interval', hours=1)
async def update_discord_users():
    """
    Updates all discord users.
    """
    for usr in User.objects(discord_user_id__ne=None):
        await utils.catch_all_async(
            update_discord_user,
            f'Could not update Discord properties of user {usr.character_name}',
            args=[usr],
        )


async def update_discord_role(grp: Group):
    """
    Updates a discord role. Makes sure all members of the group have that role,
    and demotes members that should not have it.
    """
    role = get_guild().get_role(grp.discord_role_id)
    authorized_members = [
        get_member(usr.discord_user_id) for usr in grp.members
        if usr.discord_user_id
    ]
    current_members = role.members
    for member in current_members:
        if role in member.roles:
            continue
        await member.edit(roles=list(set(member.roles) - set([role])))
    for member in authorized_members:
        if member in current_members:
            continue
        await member.edit(roles=member.roles + [role])


@scheduler.scheduled_job('interval', minutes=10)
async def update_discord_roles():
    """
    Updates discord role. A SNI group is mapped to a discord role unless that
    group's ``map_to_discord`` if ``False``
    """
    await map_discord_roles()
    for grp in Group.objects(map_to_discord=True):
        await utils.catch_all_async(
            update_discord_role,
            f'Could not update Discord role {grp.group_name}',
            args=[grp],
        )
