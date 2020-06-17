SeAT Navy Issue
===============

not affiliated with the original `SeAT <https://github.com/eveseat/seat>`_.

.. image:: https://api.codeclimate.com/v1/badges/c96b3a343687b9a4a3fa/maintainability
   :target: https://codeclimate.com/github/altaris/seat-navy-issue/maintainability
   :alt: Maintainability

.. image:: https://badgen.net/badge/icon/GitHub?icon=github&label
   :target: https://github.com/altaris/seat-navy-issue
   :alt: Repository

.. image:: https://badgen.net/badge/Python/3/blue
   :alt: Python 3

.. image:: https://badgen.net/badge/license/MIT/blue
   :target: https://choosealicense.com/licenses/mit/
   :alt: MIT License


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

   openapi
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
   configuration
   apiserver
   esi
   rest
   database


Indices and tables
------------------

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
