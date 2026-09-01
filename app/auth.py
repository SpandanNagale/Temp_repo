"""Authentication: every request carries a merchant API key or a dashboard JWT."""

import hmac
import os

import jwt
from fastapi import Header, HTTPException

JWT_ISSUER = "https://login.acme.in"


def _verify_api_key(key: str) -> str | None:
    """Return the merchant id for a valid API key."""
    merchant, _, secret = key.partition(".")
    expected = os.environ.get(f"MERCHANT_KEY_{merchant.upper()}", "")
    return merchant if expected and hmac.compare_digest(secret, expected) else None


def _verify_jwt(token: str) -> str | None:
    try:
        claims = jwt.decode(
            token, os.environ["JWT_PUBLIC_KEY"], algorithms=["RS256"], issuer=JWT_ISSUER
        )
    except jwt.PyJWTError:
        return None
    return claims.get("merchant_id")


def require_merchant(authorization: str = Header(default="")) -> str:
    """FastAPI dependency: the calling merchant's id, or 401."""
    scheme, _, value = authorization.partition(" ")
    if scheme == "ApiKey":
        merchant = _verify_api_key(value)
    elif scheme == "Bearer":
        merchant = _verify_jwt(value)
    else:
        merchant = None
    if merchant is None:
        raise HTTPException(401, "invalid credentials")
    return merchant
