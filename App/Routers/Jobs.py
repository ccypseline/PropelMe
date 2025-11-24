from fastapi import APIRouter, Depends
from typing import List
import asyncpg

from app.db import get_db
from app.schemas import JobApplication, JobApplicationBase

router = APIRouter(prefix="/jobs", tags=["jobs"])

@router.get("/", response_model=List[JobApplication])
async def list_jobs(db: asyncpg.Connection = Depends(get_db)):
    rows = await db.fetch("""
        SELECT id, company, role_title, link, status,
               contact_name, contact_linkedin_url, notes
        FROM job_applications
        ORDER BY id DESC;
    """)
    return [dict(r) for r in rows]

@router.post("/", response_model=JobApplication)
async def create_job(
    job: JobApplicationBase,
    db: asyncpg.Connection = Depends(get_db)
):
    row = await db.fetchrow("""
        INSERT INTO job_applications
            (company, role_title, link, status,
             contact_name, contact_linkedin_url, notes)
        VALUES ($1, $2, $3, $4, $5, $6, $7)
        RETURNING id, company, role_title, link, status,
                  contact_name, contact_linkedin_url, notes;
    """, job.company, job.role_title, job.link, job.status,
         job.contact_name, job.contact_linkedin_url, job.notes)
    return dict(row)
