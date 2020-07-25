"""
Token management
"""

import logging
from typing import Optional
from uuid import uuid4

import fastapi
import jwt
import jwt.exceptions as jwt_exceptions

from sni.user.models import User
import sni.conf as conf
import sni.utils as utils

from .models import StateCode, Token


def create_dynamic_app_token(
    owner: User,
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
    owner: User,
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


def create_user_token(app_token: Token, owner: User) -> Token:
    """
    Derives a new user token from an existing app token, and set the owner to
    be the user given in argument.
    """
    if app_token.token_type == Token.TokenType.dyn:
        new_token = Token(  # nosec
            created_on=utils.now(),
            expires_on=utils.now_plus(days=1),
            owner=owner,
            parent=app_token,
            token_type='use',
            uuid=str(uuid4()),
        )
    elif app_token.token_type == Token.TokenType.per:
        new_token = Token(  # nosec
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


# pylint: disable=too-many-branches
def from_authotization_header(
        authorization: str = fastapi.Header(None), ) -> Token:
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

    try:
        token = get_token_from_jwt(authorization[len(bearer):])
        logging.debug('Successfully validated token %s', token.uuid)
        return token
    except jwt_exceptions.InvalidSignatureError:
        error_msg = 'Failed to validate token: invalid signature'
    except jwt_exceptions.ExpiredSignatureError:
        error_msg = 'Failed to validate token: expired signature'
    except jwt_exceptions.InvalidAudienceError:
        error_msg = 'Failed to validate token: invalid audience'
    except jwt_exceptions.InvalidIssuerError:
        error_msg = 'Failed to validate token: invalid issuer'
    except jwt_exceptions.InvalidIssuedAtError:
        error_msg = 'Failed to validate token: invalid issuance date'
    except jwt_exceptions.ImmatureSignatureError:
        error_msg = 'Failed to validate token: immature signature'
    except jwt_exceptions.InvalidKeyError:
        error_msg = 'Failed to validate token: invalid key'
    except jwt_exceptions.InvalidAlgorithmError:
        error_msg = 'Failed to validate token: invalid algorithm'
    except jwt_exceptions.MissingRequiredClaimError:
        error_msg = 'Failed to validate token: missing claim'
    except jwt_exceptions.DecodeError:
        error_msg = 'Failed to validate token: token could not be decoded'
    except jwt_exceptions.InvalidTokenError:
        error_msg = 'Failed to validate token: token is invalid'
    except KeyError:
        error_msg = 'Failed to validate token: payload is invalid'

    logging.error(error_msg)
    raise fastapi.HTTPException(
        fastapi.status.HTTP_401_UNAUTHORIZED,
        detail=error_msg,
        headers={"WWW-Authenticate": "Bearer"},
    )


def from_authotization_header_nondyn(
        tkn: Token = fastapi.Depends(from_authotization_header), ) -> Token:
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


def get_token_from_jwt(token_str: str) -> Token:
    """
    Retrieves a token from its JWT string.
    """
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
