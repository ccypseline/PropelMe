from pydantic import BaseModel, EmailStr
from typing import Optional, Literal

WarmthBucket = Literal["hot", "warm", "cold"]
RelevanceBucket = Literal["high", "medium", "low"]

class HealthResponse(BaseModel):
    status: str

class ContactBase(BaseModel):
    name: str
    email: Optional[EmailStr] = None
    linkedin_url: Optional[str] = None
    company: Optional[str] = None
    title: Optional[str] = None
    location: Optional[str] = None

class ContactCreate(ContactBase):
    pass

class Contact(ContactBase):
    id: int
    warmth_score: float
    warmth_bucket: WarmthBucket
    relevance_score: float
    relevance_bucket: RelevanceBucket

    class Config:
        orm_mode = True

class JobApplicationBase(BaseModel):
    company: str
    role_title: str
    link: Optional[str] = None
    status: str
    contact_name: Optional[str] = None
    contact_linkedin_url: Optional[str] = None
    notes: Optional[str] = None

class JobApplication(JobApplicationBase):
    id: int

class PlannerTask(BaseModel):
    id: int
    contact_id: int
    action_type: Literal["check_profile", "comment", "message", "coffee_chat"]
    due_date: str  # ISO date string for now
    completed: bool = False
