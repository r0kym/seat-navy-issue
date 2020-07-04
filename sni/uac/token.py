"""
Token management
"""

from enum import Enum
import logging
from typing import Optional
from uuid import uuid4

import fastapi
import jwt
import jwt.exceptions
import mongoengine as me

import sni.conf as conf
import sni.utils as utils
import sni.user.user as user


class Token(me.Document):
    """
    Represents a token issued by SNI.
    """
    class TokenType(str, Enum):
        """
        Enumeration containing the various token types.
        """
        dyn = 'dyn'  # Dynamic app token
        per = 'per'  # Permanent app token
        use = 'use'  # User token

    callback = me.URLField(default=None, null=True)
    comments = me.StringField(default=str)
    created_on = me.DateTimeField(default=utils.now, required=True)
    expires_on = me.DateTimeField(default=None, null=True)
    owner = me.ReferenceField(user.User,
                              required=True,
                              reverse_delete_rule=me.CASCADE)
    parent = me.ReferenceField('self',
                               default=None,
                               null=True,
                               reverse_delete_rule=me.CASCADE)
    token_type = me.StringField(choices=TokenType, required=True)
    uuid = me.UUIDField(binary=False, unique=True)
    meta = {
        'indexes': [
            {
                'fields': ['expires_on'],
                'expireAfterSeconds': 0,
            },
        ],
    }


class StateCode(me.Document):
    """
    Represents a state code and related metadatas.

    A state code is issued when a new user token is issued from a dynamic app
    token, and is a way for SNI to remeber about the authentication while the
    end user logs in to EVE SSO.
    """
    app_token = me.ReferenceField(Token, required=True)
    created_on = me.DateTimeField(default=utils.now, required=True)
    uuid = me.UUIDField(binary=False, unique=True)
    meta = {
        'indexes': [
            {
                'fields': ['created_on'],
                'expireAfterSeconds': 600,
            },
        ],
    }


def create_dynamic_app_token(
    owner: user.User,
    *,
    callback: Optional[str] = None,
    comments: Optional[str] = None,
    parent: Optional[Token] = None,
) -> Token:
    """
    Creates a new dynamic app token for that user.

    Warning: Does not check that the user is allowed to actually do that.
    """
    new_token = Token(
        callback=callback,
        comments=comments,
        created_on=utils.now(),
        owner=owner,
        parent=parent,
        token_type=Token.TokenType.dyn,
        uuid=str(uuid4()),
    )
    new_token.save()
    logging.info('Created dynamic app token %s', new_token.uuid)
    return new_token


def create_permanent_app_token(
    owner: user.User,
    *,
    callback: Optional[str] = None,
    comments: Optional[str] = None,
    parent: Optional[Token] = None,
) -> Token:
    """
    Creates a new permanent app token for that user.

    Warning: Does not check that the user is allowed to actually do that.
    """
    new_token = Token(
        callback=callback,
        comments=comments,
        created_on=utils.now(),
        owner=owner,
        parent=parent,
        token_type=Token.TokenType.per,
        uuid=str(uuid4()),
    )
    new_token.save()
    logging.info('Created permanent app token %s', new_token.uuid)
    return new_token


def create_state_code(app_token: Token) -> StateCode:
    """
    Creates a new state code.

    See also:
        :class:`sni.uac.token.StateCode`
    """
    state_code = StateCode(
        app_token=app_token,
        created_on=utils.now(),
        uuid=str(uuid4()),
    )
    state_code.save()
    logging.info('Created state code %s for app %s', state_code.uuid,
                 app_token.uuid)
    return state_code


def create_user_token(app_token: Token, owner: user.User) -> Token:
    """
    Derives a new user token from an existing app token, and set the owner to
    be the user given in argument.
    """
    if app_token.token_type == Token.TokenType.dyn:
        new_token = Token(
            created_on=utils.now(),
            expires_on=utils.now_plus(days=1),
            owner=owner,
            parent=app_token,
            token_type='use',
            uuid=str(uuid4()),
        )
    elif app_token.token_type == Token.TokenType.per:
        new_token = Token(
            created_on=utils.now(),
            owner=owner,
            parent=app_token,
            token_type='use',
            uuid=str(uuid4()),
        )
    else:
        raise ValueError('Expected an app token')
    new_token.save()
    logging.info('Created user token %s for app %s', new_token.uuid,
                 app_token.uuid)
    return new_token


def from_authotization_header(authorization: str = fastapi.Header(
    None)) -> Token:
    """
    Validates an ``Authorization: Bearer`` header and returns a
    :class:`sni.uac.token.Token`. If the token string is invalid, raises a
    ``401``. Should be used as a FastAPI dependency.
    """
    bearer = 'Bearer '
    if not authorization or not authorization.startswith(bearer):
        raise fastapi.HTTPException(
            fastapi.status.HTTP_401_UNAUTHORIZED,
            headers={"WWW-Authenticate": "Bearer"},
        )
    token_str = authorization[len(bearer):]
    token = get_token_from_jwt(token_str)
    if not token:
        raise fastapi.HTTPException(
            fastapi.status.HTTP_401_UNAUTHORIZED,
            headers={"WWW-Authenticate": "Bearer"},
        )
    logging.debug('Successfully validated token %s', token.uuid)
    return token


def from_authotization_header_nondyn(tkn: Token = fastapi.Depends(
    from_authotization_header)) -> Token:
    """
    Validates an ``Authorization: Bearer`` header and returns a
    :class:`sni.uac.token.Token`. If the token string is invalid, or if the
    token is dynamic, raises a ``401``. Should be used as a FastAPI dependency.
    """
    if tkn.token_type == Token.TokenType.dyn:
        raise fastapi.HTTPException(
            fastapi.status.HTTP_401_UNAUTHORIZED,
            detail='Cannot use a dynamic app token for this path.')
    return tkn


def get_token_from_jwt(token_str: str) -> Optional[Token]:
    """
    Retrieves a token from its JWT string.
    """
    try:
        payload = jwt.decode(
            token_str,
            conf.get('jwt.secret'),
            algorithm=conf.get('jwt.algorithm'),
            issuer=conf.get('general.root_url'),
            verify_exp=True,
            verify_iss=True,
            verify=True,
        )
        token_uuid = payload['jti']
        return Token.objects(uuid=token_uuid).first()
    except (
            jwt.exceptions.InvalidTokenError,
            jwt.exceptions.DecodeError,
            jwt.exceptions.InvalidSignatureError,
            jwt.exceptions.ExpiredSignatureError,
            jwt.exceptions.InvalidAudienceError,
            jwt.exceptions.InvalidIssuerError,
            jwt.exceptions.InvalidIssuedAtError,
            jwt.exceptions.ImmatureSignatureError,
            jwt.exceptions.InvalidKeyError,
            jwt.exceptions.InvalidAlgorithmError,
            jwt.exceptions.MissingRequiredClaimError,
            KeyError,
    ) as error:
        logging.error('Failed validation of JWT token: %s', str(error))
        return None


def to_jwt(model: Token) -> str:
    """
    Derives a JWT token byte array from the a token model.
    """
    payload = {
        'iat': int(model.created_on.timestamp()),
        'iss': conf.get('general.root_url'),
        'jti': str(model.uuid),
        'nbf': int(model.created_on.timestamp()),
        'own': model.owner.character_id,
        'typ': model.token_type,
    }
    if model.expires_on:
        payload['exp'] = int(model.expires_on.timestamp())
    return jwt.encode(
        payload,
        conf.get('jwt.secret'),
        algorithm=conf.get('jwt.algorithm'),
    ).decode()
