from __future__ import annotations

from datetime import datetime, timezone
from typing import Optional

from fastapi import Request, Response
from pydantic import ValidationError

from app.core.auth import create_signed_token, parse_signed_token
from app.core.config import get_settings
from app.models.profile import AnonymousAssessmentCookie, AssessmentInput

COOKIE_NAME = "anon_test_data"


def create_assessment_cookie_value(assessment: AssessmentInput) -> str:
    payload = AnonymousAssessmentCookie(
        assessment=assessment,
        issued_at=datetime.now(timezone.utc),
    ).model_dump(mode="json")
    signed_value = create_signed_token(payload)
    # Browsers commonly cap an individual cookie near 4 KiB. Keep this payload small.
    if len(signed_value.encode("utf-8")) > 3800:
        raise RuntimeError("anonymous assessment cookie exceeds the safe size limit")
    return signed_value


def read_assessment_cookie(request: Request) -> Optional[AssessmentInput]:
    token = request.cookies.get(COOKIE_NAME)
    if not token:
        return None
    payload = parse_signed_token(token)
    if not payload:
        return None
    try:
        cookie = AnonymousAssessmentCookie.model_validate(payload)
    except ValidationError:
        return None
    return cookie.assessment


def set_assessment_cookie(response: Response, assessment: AssessmentInput) -> None:
    settings = get_settings()
    response.set_cookie(
        key=COOKIE_NAME,
        value=create_assessment_cookie_value(assessment),
        httponly=True,
        secure=settings.cookie_secure,
        max_age=settings.anonymous_cookie_max_age,
        samesite="lax",
        path="/",
    )
