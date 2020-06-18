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
from sni.dbmodels import Token
import sni.time as time


def create_user_token(app_token: Token) -> Token:
    """
    Derives a new user token from an existing app token.
    """
    if app_token.token_type == 'dyn':
        token = Token(
            created_on=time.now(),
            expires_on=time.now_plus(days=1),
            owner=app_token.owner,
            parent=app_token,
            token_type='use',
            uuid=str(uuid4()),
        )
        token.save()
        return token
    if app_token.token_type == 'per':
        token = Token(
            created_on=time.now(),
            owner=app_token.owner,
            parent=app_token,
            token_type='use',
            uuid=str(uuid4()),
        )
        token.save()
        return token
    raise ValueError('Expected an app token')


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
    token = validate_token(token_str)
    if not token:
        raise HTTPException(
            status.HTTP_401_UNAUTHORIZED,
            headers={"WWW-Authenticate": "Bearer"},
        )
    return token


def validate_token(token_str: str) -> Optional[Token]:
    """
    Validates a token in string form, returns the model if successful, or
    ``None`` if not.
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
