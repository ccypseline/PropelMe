# in App/Db.py
from typing import AsyncGenerator
import asyncpg
from .config import get_settings

settings = get_settings()

async def get_db() -> AsyncGenerator[asyncpg.Connection, None]:
    if not settings.db_connection_url:
        raise RuntimeError("DB_CONNECTION_URL is not set")
    conn = await asyncpg.connect(settings.db_connection_url)
    try:
        yield conn
    finally:
        await conn.close()


async def insert_job_application(conn, data: dict) -> int:
    row = await conn.fetchrow(
        """
        INSERT INTO job_applications (
            date_applied, company, job_title, job_link,
            contact_name, contact_email, hiring_manager_profile,
            jd_keywords, status, message_to_hm, notes
        ) VALUES (
            $1,$2,$3,$4,$5,$6,$7,$8,$9,$10,$11
        )
        RETURNING id
        """,
        data["date_applied"],
        data["company"],
        data["job_title"],
        data.get("job_link", ""),
        data.get("contact_name", ""),
        data.get("contact_email", ""),
        data.get("hiring_manager_profile", ""),
        data.get("jd_keywords", ""),
        data.get("status", "Planned"),
        data.get("message_to_hm", ""),
        data.get("notes", ""),
    )
    return row["id"]


async def list_job_applications(conn, status: str | None, company: str | None):
    query = "SELECT * FROM job_applications WHERE 1=1"
    params = []
    if status:
        params.append(f"%{status}%")
        query += f" AND status ILIKE ${len(params)}"
    if company:
        params.append(f"%{company}%")
        query += f" AND company ILIKE ${len(params)}"
    rows = await conn.fetch(query, *params)
    return rows


async def update_job_status(conn, job_id: int, status: str, notes_append: str | None):
    # append note
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
        job_id, status, notes_append,
    )
