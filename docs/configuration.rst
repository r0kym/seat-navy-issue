Configuration file reference
============================

.. _configuration-file-reference:

Reference
---------

The configuration file is in `YAML <https://yaml.org/>`_ format, and named
``sni.yml`` by default.

* ``database``

    * ``authentication_source`` (default: ``admin``). If the user is specific
      to the database (e.g. user ``sni`` belongs to database ``sni``), then you
      should change this to the name of the database (in this case, ``sni``).

    * ``database`` (default: ``sni``)

    * ``host``

    * ``password``

    * ``port`` (default: ``27017``)

    * ``username`` (default: ``sni``)

* ``discord``

    * ``auth_channel_id``: Authentication channel id. The bot will listen for
      ``!auth`` commands from this channel.

    * ``enabled`` (default: ``false``)

    * ``log_channel_id`` (default: ``null``): Channel id where the Discorb bot
      can send log messages.

    * ``server_id``: Server on which the bot is operating.

    * ``token``

* ``esi``: Create an application at the
  `EVE Developer Portal <https://developers.eveonline.com/>`_

    * ``client_id``

    * ``client_secret``

* ``general``

    * ``debug`` (default: ``false``): Sets the app in debug mode.

    * ``host`` (default: ``0.0.0.0``): API server host.

    * ``logging_level`` (default: ``info``)

    * ``port`` (default: ``80``): API server port.

    * ``root_url``: HTTP URL at which the API root is located (e.g.
      ``https://example.com/sni``).

    * ``scheduler_thread_count`` (default: ``5``)

* ``jwt``

    * ``algorithm`` (default: ``HS256``): A ``pyjwt`` supported algorithm, see
      `here <https://pyjwt.readthedocs.io/en/latest/algorithms.html?highlight=algorithm#digital-signature-algorithms>`_.

    * ``secret``: Application secret. Generate with ``openssl rand -hex 32``.

* ``redis``

    * ``database`` (default: ``0``).

    * ``host``

    * ``port`` (default: ``6379``).

* ``teamspeak``

    * ``auth_group_name`` (default: ``SNI TS AUTH``): Name of the auth
      group; teamspeak users authenticated through SNI are automatically added
      to this group.

    * ``bot_name`` (default: ``SeAT Navy Issue``)

    * ``enabled`` (default: ``false``)

    * ``host``

    * ``password``

    * ``port`` (default: ``10011``): The query server port! Not the port used
      by clients.

    * ``server_id`` (default: ``0``)

    * ``username`` (default: ``sni``)


.. _configuration-file-reference-example:

Example
-------

.. literalinclude:: sni.example.yml
    :language: yaml
