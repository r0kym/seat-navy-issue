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


SeAT Navy Issue is a simpler alternative to `SeAT
<https://github.com/eveseat/seat>`_. In short, it is an EVE Online community
manager, in the form of a REST API. Its core functionalities include:

* managing corporations, alliances, and even coalitions;
* creating and managing custom groups;
* storing and refreshing ESI tokens; making queries against the ESI;
* a simplistic clearance system;
* a Discord and Teamspeak connector.

Note that this project is just a backend. For a nice web-based user interface,
check out `SNI-frontend <https://github.com/r0kym/SNI-frontend>`_.


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

   Then, run::

      (your shell) > docker container exec -it mongodb bash
      (mongodb container) > mongo --username root --password rootpassword
      (mongo shell) > use sni
      (mongo shell) > db.createUser({
         user: "sni",
         pwd: "snipassword",
         roles: [
            {
                  role: "readWrite",
                  db: "sni"
            }
         ]
      })


High level documentation
------------------------

.. toctree::
   :maxdepth: 2

   command-line-arguments
   configuration
   authentication
   openapi
   todos


Module documentation
--------------------

.. toctree::
   :maxdepth: 2

   sni
   db
   user
   uac
   api
   esi
   sde
   indexation
   teamspeak
   discord


Indices and tables
------------------

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
