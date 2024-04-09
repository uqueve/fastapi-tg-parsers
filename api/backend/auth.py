from fastapi import Security, HTTPException, status
from fastapi.security import APIKeyHeader

from config_data.config import get_settings

api_key_header = APIKeyHeader(name="X-API-Key")


def check_api_key(api_key: str = Security(api_key_header)):
    settings = get_settings()
    if api_key == settings.FASTAPI_API_KEY_HEADER:
        return True
    return HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail='Missing or invalid API key'
    )
