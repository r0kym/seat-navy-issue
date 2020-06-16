"""
API Server
"""

import fastapi

app = fastapi.FastAPI()


@app.get('/ping')
async def ping():
    """
    Returns ``pong``.
    """
    return 'pong'
