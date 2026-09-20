from __future__ import annotations

from functools import lru_cache

from supabase import Client, create_client

from app.core.config import get_settings


@lru_cache(maxsize=1)
def get_supabase() -> Client:
    """Return the normal Supabase client configured with the public/anon key."""
    settings = get_settings()
    url, key = settings.require_supabase_anon_config()
    return create_client(url, key)


@lru_cache(maxsize=1)
def get_supabase_admin() -> Client:
    """Return the privileged client; never silently downgrade to the anon client."""
    settings = get_settings()
    url, key = settings.require_supabase_admin_config()
    return create_client(url, key)
