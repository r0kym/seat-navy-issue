Configuration facility
======================

.. _configuration-file-reference:

Reference
---------

The configuration file is in `YAML <https://yaml.org/>`_ format, and named
``sni.yml`` by default.

* ``database``
    * ``authentication_source`` (default: ``admin``)
    * ``database`` (default: ``sni``)
    * ``host``
    * ``password``
    * ``port`` (default: ``27017``)
    * ``username`` (default: ``sni``)
* ``esi``: Create an application at the `EVE Developer Portal <https://developers.eveonline.com/>`_
    * ``client_id``
    * ``client_secret``
* ``general``
    * ``debug`` (default: ``false``): Sets the app in debug mode.
    * ``host`` (default: ``0.0.0.0``): API server host.
    * ``port`` (default: ``80``): API server port.
    * ``root_url``: HTTP URL at which the API root is located (e.g.
      ``https://example.com/sni``)
    * ``scheduler_thread_count`` (default: ``5``)
* ``jwt``
    * ``algorithm`` (default: ``HS256``): A ``pyjwt`` supported algorithm, see `here <https://pyjwt.readthedocs.io/en/latest/algorithms.html?highlight=algorithm#digital-signature-algorithms>`_.
    * ``secret``: Application secret. Generate with ``openssl rand -hex 32``.
* ``logging``: Logging facility configuration, see the `logging.config documentation <https://docs.python.org/3/library/logging.config.html#dictionary-schema-details>`_.
* ``redis``
    * ``database`` (default: ``0``)
    * ``host``
    * ``port`` (default: ``6379``)
* ``teamspeak``
    * ``enabled`` (default: ``false``)
    * ``host``
    * ``password``
    * ``port``
    * ``username``


.. _configuration-file-reference-example:

Example
-------

.. literalinclude:: sni.example.yml
    :language: yaml


Module documentation
--------------------

.. automodule:: sni.conf
