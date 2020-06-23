User Access Control
===================

.. _users-groups-etc:

Users, groups, etc.
-------------------

.. image:: users.png

Access control
--------------

An *access* is comprised of the following.

* An **actor**, that wishes to perform a certain action. In the database,
  actors are represented as a string ``type:id``, where ``type`` is either
  ``all`` (alliance), ``chr`` (character), ``coa`` (coalition), ``crp``
  (corporation), ``grp`` (group), and where ``id`` is the id of the entity in
  the relevant table (see :ref:`users-groups-etc`).

* An **API endpoint** whose access is controlled.

* A **scope**, within which the action can be performed by the actor. This is a
  tuple ``type:id`` as above.

For example, the access

===========  ==========================================  ===========
``actor``    ``endpoint``                                ``scope``
===========  ==========================================  ===========
``grp:123``  ``/esi/characters/{character_id}/assets/``  ``crp:456``
===========  ==========================================  ===========

means that all characters of group ``123`` can issue the
``/esi/characters/{character_id}/assets/`` request (which proxies to the
``/characters/{character_id}/assets/`` ESI request) against all characters of
corporation ``456``.

.. warning::
    Endpoint names are actually stored in a separate table, and referred to
    using their id.


UAC modules documentation
-------------------------

``sni.uac.token``
~~~~~~~~~~~~~~~~~

.. automodule:: sni.uac.token

``sni.uac.user``
~~~~~~~~~~~~~~~~

.. automodule:: sni.uac.user