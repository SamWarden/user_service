from dataclasses import dataclass
import os

from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer


@dataclass
class ApiKeyAuth:
    """API Key authentication dependency for protecting service endpoints."""

    api_key: str

    @classmethod
    def from_env(cls) -> "ApiKeyAuth":
        api_key = os.getenv("API_KEY", "")
        if not api_key:
            raise RuntimeError(
                "API_KEY environment variable is not set. "
                "Generate one with: python -c 'import secrets; print(secrets.token_urlsafe(32))'"
            )
        return cls(api_key=api_key)

    async def __call__(
        self,
        credentials: HTTPAuthorizationCredentials = Depends(HTTPBearer()),
    ) -> None:
        if credentials.credentials != self.api_key:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid API key",
            )


def get_api_key_auth() -> ApiKeyAuth:
    """Factory for ApiKeyAuth dependency."""
    return ApiKeyAuth.from_env()
