"""
Manages the issuance and validation of JWT tokens
"""

import jwt

import sni.conf as conf
import sni.dbmodels as dbmodels


def to_jwt(model: dbmodels.Token) -> str:
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
