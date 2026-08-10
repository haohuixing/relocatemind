import os
from dotenv import load_dotenv
from supabase import create_client, Client

load_dotenv()

SUPABASE_URL = os.getenv("SUPABASE_URL", "https://your-project-ref.supabase.co")
SUPABASE_KEY = (
    os.getenv("SUPABASE_ANON_KEY")
    or os.getenv("SUPABASE_KEY")
    or "your-supabase-anon-key"
)
SUPABASE_SERVICE_ROLE_KEY = os.getenv("SUPABASE_SERVICE_ROLE_KEY", "")

# Standard client (respects RLS)
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

# Admin client (bypasses RLS for server-side profile creation during signup)
supabase_admin: Client = (
    create_client(SUPABASE_URL, SUPABASE_SERVICE_ROLE_KEY)
    if SUPABASE_SERVICE_ROLE_KEY
    else supabase
)


def get_supabase() -> Client:
    """Dependency helper to return initialized Supabase client."""
    return supabase