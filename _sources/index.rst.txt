SeAT Navy Issue
===============

not affiliated with the original `SeAT <https://github.com/eveseat/seat>`_.


Running SNI
-----------

1. Register an application at the
   `EVE Developer Portal <https://developers.eveonline.com/>`_. The SNI
   callback is ``https://<domain>/callback/esi``.
2. Create a configuration file (see :ref:`configuration-file-reference`).
3. The easiest way to run SNI and all the required services is to use the
   following docker-compose file: (don't forget to change the password to match
   that of your ``sni.yml``)

.. literalinclude:: docker-compose.example.yml
   :language: yaml


High level documentation
------------------------

.. toctree::
   :maxdepth: 2

   configuration
   authentication
   users
   uac
   todos


Module documentation
--------------------

.. toctree::
   :maxdepth: 2

   sni


Indices and tables
------------------

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
