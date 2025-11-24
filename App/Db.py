import asyncpg
from typing import AsyncGenerator
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
