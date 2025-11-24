from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import os
import asyncpg

app = FastAPI(title="PropelMe Backend")

# CORS – allow your frontend + localhost for now
origins = [
    "http://localhost:3000",
    "http://127.0.0.1:3000",
    # add your future Cloud Run / Firebase hosting URLs here
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

DATABASE_URL = os.getenv("DB_CONNECTION_URL")

async def get_db():
    if not DATABASE_URL:
        raise RuntimeError("DB_CONNECTION_URL not set")
    conn = await asyncpg.connect(DATABASE_URL)
    try:
        yield conn
    finally:
        await conn.close()

class HealthResponse(BaseModel):
    status: str

@app.get("/health", response_model=HealthResponse)
async def health():
    return HealthResponse(status="ok")

# Example: list contacts (schema to be added later)
@app.get("/contacts")
async def list_contacts(db = Depends(get_db)):
    rows = await db.fetch("SELECT id, name, email FROM contacts LIMIT 50;")
    return [dict(r) for r in rows]
