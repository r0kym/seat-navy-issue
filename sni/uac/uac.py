"""
General user access control methods
"""

from typing import Optional

from sni.user.models import Group, User


# pylint: disable=too-many-return-statements
def is_authorized_to_login(usr: User) -> bool:
    """
    Tells wether a user is authorized to login or not. A user is authorized to
    login if the following conditions are satisfied:

    * its ``authorized_to_login`` field is ``True`` or if the user belongs to
      **at least one** group, corporation, alliance, or coalition whose
      ``authorized_to_login`` field is ``True``;

    * the user's ``authorized_to_login`` field is not ``False``, and none of
      the groups, corporation, alliance, or coalitions the user belongs to has
      a ``authorized_to_login`` field set ot ``False``.

    In addition, the root user is always allowed to login, regardless of the
    status of the group he's part of.
    """
    if usr.character_id == 0:
        return True

    if usr.authorized_to_login is False:
        return False

    authorized_to_login: Optional[bool] = usr.authorized_to_login

    if usr.corporation is not None:
        if usr.corporation.authorized_to_login is False:
            return False
        # Note that in Python, (None or True) == True
        authorized_to_login = authorized_to_login or usr.corporation.authorized_to_login

    if usr.alliance is not None:
        if usr.alliance.authorized_to_login is False:
            return False
        authorized_to_login = authorized_to_login or usr.alliance.authorized_to_login

    for coa in usr.coalitions():
        if coa.authorized_to_login is False:
            return False
        authorized_to_login = authorized_to_login or coa.authorized_to_login

    for grp in Group.objects(members=usr):
        if grp.authorized_to_login is False:
            return False
        authorized_to_login = authorized_to_login or grp.authorized_to_login

    # If authorized_to_login is still None, then the result is False
    return bool(authorized_to_login)
