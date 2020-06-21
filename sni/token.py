"""
Manages the issuance and validation of JWT tokens
"""

import logging
from typing import Optional
from uuid import uuid4

from fastapi import (
    Header,
    HTTPException,
    status,
)
import jwt
import jwt.exceptions

import sni.conf as conf
from sni.dbmodels import StateCode, Token, User
import sni.time as time


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
        created_on=time.now(),
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
        created_on=time.now(),
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
        :class:`sni.dbmodels.StateCode`
    """
    state_code = StateCode(
        app_token=app_token,
        created_on=time.now(),
        uuid=str(uuid4()),
    )
    state_code.save()
    logging.info('Created state code %s for app %s', state_code.uuid,
                 app_token.uuid)
    return state_code


def create_user_token(app_token: Token) -> Token:
    """
    Derives a new user token from an existing app token.
    """
    if app_token.token_type == Token.TokenType.dyn:
        new_token = Token(
            created_on=time.now(),
            expires_on=time.now_plus(days=1),
            owner=app_token.owner,
            parent=app_token,
            token_type='use',
            uuid=str(uuid4()),
        )
    elif app_token.token_type == Token.TokenType.per:
        new_token = Token(
            created_on=time.now(),
            owner=app_token.owner,
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


def delete_token(uuid: str) -> bool:
    """
    Deletes a token by its uuid.

    Returns:
        Wether the deletion was successful.
    """
    to_delete = Token.objects(uuid=uuid).first()
    if not to_delete:
        return False
    to_delete.delete()
    logging.debug('Deleted token %s', uuid)
    return True


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


def validate_header(authorization: str = Header(None)) -> Token:
    """
    Validates an ``Authorization: Bearer`` header.

    Should be used as a FastAPI dependency.
    """
    bearer = 'Bearer '
    if not authorization or not authorization.startswith(bearer):
        raise HTTPException(
            status.HTTP_401_UNAUTHORIZED,
            headers={"WWW-Authenticate": "Bearer"},
        )
    token_str = authorization[len(bearer):]
    token = get_token_from_jwt(token_str)
    if not token:
        raise HTTPException(
            status.HTTP_401_UNAUTHORIZED,
            headers={"WWW-Authenticate": "Bearer"},
        )
    logging.debug('Successfully validated token %s', token.uuid)
    return token