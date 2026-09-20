from __future__ import annotations

import os
from dataclasses import dataclass
from functools import lru_cache

from dotenv import load_dotenv


_INSECURE_SECRET_VALUES = {
    "",
    "relocation-app-secret-key-change-in-prod",
    "change-me",
    "change-me-in-production",
}


def _env_bool(name: str, default: bool = False) -> bool:
    value = os.getenv(name)
    if value is None:
        return default
    return value.strip().lower() in {"1", "true", "yes", "on"}


@dataclass(frozen=True)
class Settings:
    """Application configuration loaded from environment variables."""

    app_env: str
    supabase_url: str
    supabase_anon_key: str
    supabase_service_role_key: str
    secret_key: str
    cookie_secure_override: bool | None
    anonymous_cookie_max_age: int

    @property
    def is_production(self) -> bool:
        return self.app_env.lower() in {"production", "prod"}

    @property
    def cookie_secure(self) -> bool:
        if self.cookie_secure_override is not None:
            return self.cookie_secure_override
        return self.is_production

    def validate_for_startup(self) -> None:
        """Fail fast for missing production configuration without exposing values."""
        if not self.is_production:
            return

        missing = []
        if not self.supabase_url:
            missing.append("SUPABASE_URL")
        if not self.supabase_anon_key:
            missing.append("SUPABASE_ANON_KEY")
        if not self.supabase_service_role_key:
            missing.append("SUPABASE_SERVICE_ROLE_KEY")
        if self.secret_key in _INSECURE_SECRET_VALUES:
            missing.append("SECRET_KEY")

        if missing:
            names = ", ".join(missing)
            raise RuntimeError(f"Missing or insecure production configuration: {names}")

    def require_secret_key(self) -> str:
        if self.secret_key in _INSECURE_SECRET_VALUES:
            raise RuntimeError("SECRET_KEY must be configured before signing application data")
        return self.secret_key

    def require_supabase_anon_config(self) -> tuple[str, str]:
        if not self.supabase_url or not self.supabase_anon_key:
            raise RuntimeError("SUPABASE_URL and SUPABASE_ANON_KEY must be configured")
        return self.supabase_url, self.supabase_anon_key

    def require_supabase_admin_config(self) -> tuple[str, str]:
        if not self.supabase_url or not self.supabase_service_role_key:
            raise RuntimeError(
                "SUPABASE_URL and SUPABASE_SERVICE_ROLE_KEY must be configured for admin operations"
            )
        return self.supabase_url, self.supabase_service_role_key


@lru_cache(maxsize=1)
def get_settings() -> Settings:
    load_dotenv()
    secure_override = os.getenv("COOKIE_SECURE")
    return Settings(
        app_env=os.getenv("APP_ENV", "development").strip().lower(),
        supabase_url=os.getenv("SUPABASE_URL", "").strip(),
        supabase_anon_key=(os.getenv("SUPABASE_ANON_KEY") or os.getenv("SUPABASE_KEY", "")).strip(),
        supabase_service_role_key=os.getenv("SUPABASE_SERVICE_ROLE_KEY", "").strip(),
        secret_key=os.getenv("SECRET_KEY", "").strip(),
        cookie_secure_override=(
            _env_bool("COOKIE_SECURE") if secure_override is not None else None
        ),
        anonymous_cookie_max_age=max(60, int(os.getenv("ANONYMOUS_COOKIE_MAX_AGE", "3600"))),
    )
