import base64
import hashlib
import hmac
import json
from typing import Optional, Dict, Any

from fastapi import Request

from app.core.config import get_settings
from app.database import get_supabase


def _secret_key() -> str:
    return get_settings().require_secret_key()


def create_signed_token(data: dict) -> str:
    """Creates HMAC-signed base64 tokens for anonymous test cookies."""
    json_bytes = json.dumps(data).encode("utf-8")
    b64_payload = base64.urlsafe_b64encode(json_bytes).decode("utf-8")
    signature = hmac.new(
        _secret_key().encode(), b64_payload.encode(), hashlib.sha256
    ).hexdigest()
    return f"{b64_payload}.{signature}"


def parse_signed_token(token: str) -> Optional[dict]:
    """Parses and verifies HMAC-signed base64 tokens."""
    if not token or "." not in token:
        return None
    try:
        b64_payload, signature = token.split(".", 1)
        expected_sig = hmac.new(
            _secret_key().encode(), b64_payload.encode(), hashlib.sha256
        ).hexdigest()
        if hmac.compare_digest(signature, expected_sig):
            json_bytes = base64.urlsafe_b64decode(b64_payload)
            return json.loads(json_bytes.decode("utf-8"))
    except Exception:
        return None
    return None


def get_current_user(request: Request) -> Optional[Dict[str, Any]]:
    """
    Retrieves authenticated Supabase user using access token stored in HTTP-only cookie.
    """
    token = request.cookies.get("sb_access_token")
    if not token:
        return None
    try:
        response = get_supabase().auth.get_user(token)
        if response and response.user:
            return {
                "id": response.user.id,
                "email": response.user.email,
            }
    except Exception:
        return None
    return None


# Naming alias for backwards compatibility
get_current_user_session = get_current_user


def get_current_user_id(request: Request) -> Optional[str]:
    """Helper returning current user's UUID string from Supabase."""
    user = get_current_user(request)
    return user["id"] if user else None