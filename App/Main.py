from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.schemas import HealthResponse
from app.routers import contacts, jobs, planner

app = FastAPI(title="PropelMe Backend")

# CORS – adjust origins as needed
origins = [
    "http://localhost:3000",
    "http://127.0.0.1:3000",
    # Add your Cloud Run / Firebase hosting domain later
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/health", response_model=HealthResponse)
async def health():
    return HealthResponse(status="ok")

# Routers
app.include_router(contacts.router)
app.include_router(jobs.router)
app.include_router(planner.router)
