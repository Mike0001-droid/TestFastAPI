from fastapi import HTTPException, status, Security
from fastapi.security import APIKeyHeader, APIKeyQuery
from core.config import settings


api_key_query = APIKeyQuery(name="api-key", auto_error=False)
api_key_header = APIKeyHeader(name="x-api-key", auto_error=False)


def get_api_key(
        api_key_query: str = Security(api_key_query),
        api_key_header: str = Security(api_key_header),
    ):
    if api_key_query == settings.api_key:
        return api_key_query
    if api_key_header == settings.api_key:
        return api_key_header
    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Invalid or missing API Key",
    )


