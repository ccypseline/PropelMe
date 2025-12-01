# App/Db.py
from typing import AsyncGenerator, Optional, List, Any, Dict
import asyncpg
from .config import get_settings  # make sure file is app/config.py (lowercase)

settings = get_settings()


async def get_db() -> AsyncGenerator[asyncpg.Connection, None]:
    """
    FastAPI dependency: yields an asyncpg connection and closes it afterwards.
    """
    if not settings.db_connection_url:
        raise RuntimeError("DB_CONNECTION_URL is not set")
    conn = await asyncpg.connect(settings.db_connection_url)
    try:
        yield conn
    finally:
        await conn.close()


# -------- Job applications helpers --------

async def insert_job_application(
    conn: asyncpg.Connection,
    data: Dict[str, Any],
) -> Dict[str, Any]:
    """
    Insert a job application row and return the inserted record as dict.
    Expects keys: company, role_title, link, status, contact_name,
                  contact_linkedin_url, notes
    """
    row = await conn.fetchrow(
        """
        INSERT INTO job_applications (
            company,
            role_title,
            link,
            status,
            contact_name,
            contact_linkedin_url,
            notes
        )
        VALUES ($1,$2,$3,$4,$5,$6,$7)
        RETURNING id,
                  company,
                  role_title,
                  link,
                  status,
                  contact_name,
                  contact_linkedin_url,
                  notes;
        """,
        data["company"],
        data["role_title"],
        data.get("link", ""),
        data.get("status", "Planned"),
        data.get("contact_name", ""),
        data.get("contact_linkedin_url", ""),
        data.get("notes", ""),
    )
    return dict(row)


async def list_job_applications(
    conn: asyncpg.Connection,
) -> list[Dict[str, Any]]:
    rows = await conn.fetch(
        """
        SELECT id,
               company,
               role_title,
               link,
               status,
               contact_name,
               contact_linkedin_url,
               notes
        FROM job_applications
        ORDER BY id DESC;
        """
    )
    return [dict(r) for r in rows]


async def update_job_status(
    conn: asyncpg.Connection,
    job_id: int,
    status: str,
    notes_append: Optional[str] = None,
) -> Dict[str, Any]:
    """
    Update status (and optionally append to notes), then return updated row.
    """
    await conn.execute(
        """
        UPDATE job_applications
        SET status = $2,
            notes = CASE
                        WHEN $3 IS NULL OR $3 = '' THEN notes
                        ELSE COALESCE(notes, '') || '\n' || $3
                    END
        WHERE id = $1
        """,
        job_id,
        status,
        notes_append,
    )

    row = await conn.fetchrow(
        """
        SELECT id,
               company,
               role_title,
               link,
               status,
               contact_name,
               contact_linkedin_url,
               notes
        FROM job_applications
        WHERE id = $1
        """,
        job_id,
    )
    return dict(row) if row else {}
