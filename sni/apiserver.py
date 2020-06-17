"""
API Server
"""

import logging
from uuid import uuid4

import fastapi

import sni.apimodels as apimodels
import sni.esi as esi

app = fastapi.FastAPI()


@app.get('/auth', response_model=apimodels.AuthOut)
async def auth(data: apimodels.AuthIn):
    """
    Initiates the user authentication process. Returns a user token.
    """
    uuid = str(uuid4())
    return {
        'login_url': esi.get_auth_url(data.scopes, uuid),
        'user_token': uuid,
        'user_token_valid': False,
    }


@app.get('/callback/esi')
async def callback_esi(code: str, state: str):
    """
    ESI callback.
    """
    logging.info('Received callback from ESI for state %s', state)
    esi.process_sso_authorization_code(code, state)
    return {}


@app.get('/ping')
async def ping():
    """
    Returns ``pong``.
    """
    return 'pong'
