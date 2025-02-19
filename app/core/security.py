from fastapi import HTTPException, Security
from fastapi.security import APIKeyHeader
from app.core.config import get_settings

settings = get_settings()
api_key_header = APIKeyHeader(name="Authorization", auto_error=False)

async def verify_password(token: str) -> bool:
    """Verify the bearer token against the configured password"""
    expected = f"Bearer {settings.AUTH_PASSWORD}"
    if not token or token != expected:
        raise HTTPException(
            status_code=401,
            detail="Invalid authentication credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return True

def verify_password_old(password: str) -> bool:
    """Verify the password against the configured password"""
    return password == settings.AUTH_PASSWORD 