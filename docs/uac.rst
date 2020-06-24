User Access Control
===================

.. _users-groups-etc:

Users, groups, etc.
-------------------

.. image:: users.png


Clearance levels
----------------

Each user has a **clearance level**, which is an integer:

* Level 0: User only have access to public data and read-write access to its
  own ESI.

* Level 1: User has access to read-only ESI (i.e. ``GET`` calls) of all members
  of his corporation.

* Level 2: User has access to read-write ESI (i.e. all http methods) of all
  members of his corporation.

* Level 3: User has access to read-only ESI (i.e. ``GET`` calls) of all members
  of his alliance.

* Level 4: User has access to read-write ESI (i.e. all http methods) of all
  members of his alliance.

* Level 5: User has access to read-only ESI (i.e. ``GET`` calls) of all members
  of his coalition.

* Level 6: User has access to read-write ESI (i.e. all http methods) of all
  members of his coalition.

* Level 7: User has access to read-only ESI (i.e. ``GET`` calls) of all members
  regisered on this SNI instance.

* Level 8: User has access to read-write ESI (i.e. all http methods) of all
  members regisered on this SNI instance.

* Level 9: User has clearance level 8 and some administrative priviledges.

* Level 10: Superuser.

Furthermore, note that

* Any user can raise any other to its own clearance level, provided they are in
  the same corporation (for levels 1 and 2), alliance (for levels 3 and 4), or
  coalition (for levels 5 and 6).

* Demoting users is considered an administrative task and requires a clearance
  of at least 9.

* Clearance levels are public informations.


See :meth:`sni.uac.clearance.has_clearance` for a precise specification of how
clearance levels are checked, and :car:`sni.uac.clearance.SCOPE_LEVELS` for the
declaration of all scopes.


UAC modules documentation
-------------------------

``sni.uac.token``
~~~~~~~~~~~~~~~~~

.. automodule:: sni.uac.token

``sni.uac.user``
~~~~~~~~~~~~~~~~

.. automodule:: sni.uac.user
