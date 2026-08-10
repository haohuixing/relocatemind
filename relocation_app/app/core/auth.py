import base64
import hashlib
import hmac
import json
from typing import Optional
from fastapi import Request
from passlib.context import CryptContext

SECRET_KEY = "relocation-app-secret-key-change-in-prod"
pwd_context = CryptContext(schemes=["pbkdf2_sha256"], deprecated="auto")


def hash_password(password: str) -> str:
    return pwd_context.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)


def create_signed_token(data: dict) -> str:
    json_bytes = json.dumps(data).encode("utf-8")
    b64_payload = base64.urlsafe_b64encode(json_bytes).decode("utf-8")
    signature = hmac.new(
        SECRET_KEY.encode(), b64_payload.encode(), hashlib.sha256
    ).hexdigest()
    return f"{b64_payload}.{signature}"


def parse_signed_token(token: str) -> Optional[dict]:
    if not token or "." not in token:
        return None
    try:
        b64_payload, signature = token.split(".", 1)
        expected_sig = hmac.new(
            SECRET_KEY.encode(), b64_payload.encode(), hashlib.sha256
        ).hexdigest()
        if hmac.compare_digest(signature, expected_sig):
            json_bytes = base64.urlsafe_b64decode(b64_payload)
            return json.loads(json_bytes.decode("utf-8"))
    except Exception:
        return None
    return None


def get_current_user_id(request: Request) -> Optional[int]:
    session_cookie = request.cookies.get("session_token")
    if not session_cookie:
        return None
    payload = parse_signed_token(session_cookie)
    if payload and "user_id" in payload:
        return payload["user_id"]
    return None
