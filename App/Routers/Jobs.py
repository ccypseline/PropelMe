# app/routers/jobs.py  (or similar)

from fastapi import APIRouter, Depends, HTTPException
from typing import List
import asyncpg

from App.Db import (
    get_db,
    list_job_applications,
    insert_job_application,
    update_job_status,
)
from App.Schemas import JobApplication, JobApplicationBase

# ⚠️ Adjust this import to match your actual file layout.
# For example, if your agent lives at:
#   app/agents/gemini_agent.py   with class GeminiAgent
# then this import is correct:
from App.Agents.gemini_agent import GeminiAgent

router = APIRouter(prefix="/jobs", tags=["jobs"])

gemini = GeminiAgent()


@router.get("/", response_model=List[JobApplication])
async def list_jobs(db: asyncpg.Connection = Depends(get_db)):
    rows = await list_job_applications(db)
    return rows


@router.post("/", response_model=JobApplication)
async def create_job(
    job: JobApplicationBase,
    db: asyncpg.Connection = Depends(get_db),
):
    data = {
        "company": job.company,
        "role_title": job.role_title,
        "link": job.link,
        "status": job.status,
        "contact_name": job.contact_name,
        "contact_linkedin_url": job.contact_linkedin_url,
        "notes": job.notes,
    }
    row = await insert_job_application(db, data)
    return row


@router.post("/{job_id}/status", response_model=JobApplication)
async def update_job(
    job_id: int,
    body: dict,
    db: asyncpg.Connection = Depends(get_db),
):
    """
    Update status and optionally append a note.
    Body expects:
    {
      "status": "Interview",
      "notes_append": "Had first screening call"
    }
    """
    if "status" not in body:
        raise HTTPException(status_code=400, detail="status is required")

    row = await update_job_status(
        db,
        job_id=job_id,
        status=body["status"],
        notes_append=body.get("notes_append"),
    )
    if not row:
        raise HTTPException(status_code=404, detail="Job not found")
    return row


@router.post("/parse")
async def parse(body: dict):
    """
    Use Gemini to parse free-text job description / notes into structured fields.
    Body:
    { "text": "..." }
    """
    text = body.get("text", "")
    if not text:
        raise HTTPException(status_code=400, detail="text is required")
    return gemini.extract_application_fields(text)


@router.post("/draft-message")
async def draft(body: dict):
    """
    Use Gemini to draft a LinkedIn message to a hiring manager.
    Body expects:
    {
      "your_background": "...",
      "company": "...",
      "job_title": "...",
      "hiring_manager_name": "...",   # optional
      "jd_keywords": "..."            # optional
    }
    """
    for field in ["your_background", "company", "job_title"]:
        if field not in body:
            raise HTTPException(status_code=400, detail=f"{field} is required")

    msg = gemini.draft_job_message(
        your_background=body["your_background"],
        company=body["company"],
        job_title=body["job_title"],
        hiring_manager_name=body.get("hiring_manager_name", ""),
        jd_keywords=body.get("jd_keywords", ""),
    )
    return {"message": msg}
