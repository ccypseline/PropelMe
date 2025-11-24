from fastapi import APIRouter, Depends
from typing import List
import asyncpg

from app.db import get_db
from app.schemas import PlannerTask

router = APIRouter(prefix="/planner", tags=["planner"])

@router.get("/tasks", response_model=List[PlannerTask])
async def list_tasks(db: asyncpg.Connection = Depends(get_db)):
    rows = await db.fetch("""
        SELECT id, contact_id, action_type,
               to_char(due_date, 'YYYY-MM-DD') AS due_date,
               completed
        FROM planner_tasks
        ORDER BY due_date ASC;
    """)
    return [dict(r) for r in rows]
