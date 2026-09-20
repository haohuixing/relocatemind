from supabase import Client

from app.database import get_supabase, get_supabase_admin


# Backward-compatible names for code migrating to app.database.
def get_supabase_client() -> Client:
    return get_supabase()


def get_supabase_admin_client() -> Client:
    return get_supabase_admin()
