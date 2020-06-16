Authentication
==============

An application that wishes to use SNI must use an *app token* in order to get a
*user token*, with which API request can be done. There are two kinds of app tokens.

* **Permanent app token**: this token is tied to a user, and inherits the
  privileges of that user.

  .. uml::

    title Authentication with a permanent token

    actor Application
    participant SNI

    Application -> SNI : POST /auth + app token
    SNI -> Application : **200** + user token + metadatas

* **Dynamic app token**: this token is tied to ``root``, and requires the user to
  authenticate via the ESI SSO; the user token inherits the privileges of the
  user that logged in.

  .. uml::

    title Authentication with a dynamic token

    actor User
    actor Application
    participant SNI
    participant "EVE SSO"

    Application -> SNI : POST /auth + app token
    SNI -> Application : **200** + EVE SSO URL + user token
    note left : The user token is invalid until the authentication is complete

    Application -> User : Application forwards login URL

    group Standard EVE SSO authentication flow
        User -> "EVE SSO" : User logs in
        "EVE SSO" -> SNI : GET request to SNI auth callback + authorization code
        SNI -> "EVE SSO" : POST request with authentication code
        "EVE SSO" -> SNI : Access token + refresh token
        note left : User token issued in is now valid
    end

    SNI -> Application : GET request to callback, notifying auth. status

    group Testing a user token
        Application -> SNI : /auth + user token
        SNI -> Application : **200** + metadatas
    else user token not valid (yet)
        SNI -> Application : **401**
    end

App and user tokens take the form of a JWT bearer token, and must be included
to requests under the ``Authorization`` header: ::

    Authorization: Bearer <token>

User s deriving from a permanent app tokens are themselves permanent, but
expire after 48h of inactivity. User tokens deriving from dynamic app tokens
are valid for 24h. Note that user and app tokens can be manyally revoked. If an
app token is revoked, then user tokens deriving from it are also revoked.
