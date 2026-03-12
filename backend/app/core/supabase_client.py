from functools import lru_cache
from typing import Optional

from supabase import create_client, Client

from app.core.config import settings


# ------------------------------------------------------------------
# Client Creation
# ------------------------------------------------------------------

def _create_supabase_client() -> Client:

    if not settings.SUPABASE_URL or not settings.SUPABASE_KEY:
        raise RuntimeError("Supabase credentials not configured")

    return create_client(
        settings.SUPABASE_URL,
        settings.SUPABASE_KEY,
    )


@lru_cache
def get_supabase_client() -> Client:
    """
    Cached Supabase client instance.
    Safe for FastAPI dependency injection.
    """
    return _create_supabase_client()


# Global access (for repositories/services)
supabase: Client = get_supabase_client()


# ------------------------------------------------------------------
# Storage Helpers
# ------------------------------------------------------------------

REPORTS_BUCKET = "reports"


def upload_pdf(path: str, pdf_bytes: bytes) -> str:
    """
    Upload a PDF to Supabase Storage and return its public URL.
    """

    result = supabase.storage.from_(REPORTS_BUCKET).upload(
        path,
        pdf_bytes,
        {"content-type": "application/pdf"},
    )

    if hasattr(result, "error") and result.error:
        raise RuntimeError(result.error)

    return get_public_url(path)


def get_public_url(path: str) -> str:
    """
    Return public URL for stored file.
    """

    res = supabase.storage.from_(REPORTS_BUCKET).get_public_url(path)

    # Supabase python client returns dict-like structure
    if isinstance(res, dict):
        return res.get("publicURL") or res.get("public_url")

    return res