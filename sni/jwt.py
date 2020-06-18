"""
Manages the issuance and validation of JWT tokens
"""

import logging
from typing import Optional

import jwt
import jwt.exceptions

import sni.conf as conf
from sni.dbmodels import Token


def to_jwt(model: Token) -> str:
    """
    Derives a JWT token byte array from the a token model.
    """
    return jwt.encode(
        {
            'created_on': str(model.created_on),
            'expires_on': str(model.expires_on),
            'owner': model.owner.character_id,
            'token_type': model.token_type,
            'uuid': str(model.uuid),
        },
        conf.get('jwt.secret'),
        algorithm=conf.get('jwt.algorithm'),
    ).decode()


def validate(token: str) -> Optional[Token]:
    """
    Validates a token in string form, returns the model if successful, or
    ``None`` if not.
    """
    try:
        payload = jwt.decode(
            token.encode(),
            conf.get('jwt.secret'),
            algorithm=conf.get('jwt.algorithm'),
            verify_signature=True,
        )
        token_uuid = payload['uuid']
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
