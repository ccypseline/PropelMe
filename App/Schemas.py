cat > App/Schemas.py << 'EOF'
from pydantic import BaseModel, EmailStr, Field
from typing import Optional, Literal, List
from datetime import datetime
from enum import Enum

# Your existing types
WarmthBucket = Literal["hot", "warm", "cold"]
RelevanceBucket = Literal["high", "medium", "low"]

# New enums for extended functionality
class RelationshipType(str, Enum):
    CLOSE_FRIEND = "close_friend"
    FRIEND = "friend"
    FORMER_COLLEAGUE = "former_colleague"
    CURRENT_COLLEAGUE = "current_colleague"
    ACQUAINTANCE = "acquaintance"
    MET_ONCE = "met_once"
    NEVER_MET = "never_met"

class ContactSource(str, Enum):
    LINKEDIN = "linkedin"
    MANUAL = "manual"
    CSV_IMPORT = "csv_import"
    EVENTBRITE = "eventbrite"

# Your existing models
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
    id: Optional[int] = None
    warmth_score: float = 0.0
    warmth_bucket: Optional[WarmthBucket] = None
    relevance_score: float = 0.0
    relevance_bucket: Optional[RelevanceBucket] = None
    
    # Extended fields for prioritization
    relationship: Optional[RelationshipType] = None
    last_interaction_date: Optional[datetime] = None
    interaction_count: int = 0
    priority_score: float = 0.0
    source: ContactSource = ContactSource.MANUAL
    tags: List[str] = []
    notes: Optional[str] = None
    created_at: Optional[datetime] = Field(default_factory=datetime.now)
    updated_at: Optional[datetime] = Field(default_factory=datetime.now)

    class Config:
        from_attributes = True  # Updated from orm_mode for Pydantic v2

class JobApplicationCreate(BaseModel):
    date_applied: date
    company: str
    job_title: str
    job_link: Optional[str] = ""
    contact_name: Optional[str] = ""
    contact_email: Optional[str] = ""
    hiring_manager_profile: Optional[str] = ""
    jd_keywords: Optional[str] = ""
    status: str = "Planned"
    message_to_hm: Optional[str] = ""
    notes: Optional[str] = ""

class JobApplication(JobApplicationBase):
    id: int

    class Config:
        from_attributes = True

class PlannerTask(BaseModel):
    id: Optional[int] = None
    contact_id: int
    action_type: Literal["check_profile", "comment", "message", "coffee_chat"]
    due_date: str  # ISO date string
    completed: bool = False

    class Config:
        from_attributes = True

# New models for extended functionality
class Interaction(BaseModel):
    id: Optional[str] = None
    contact_id: int
    date: datetime = Field(default_factory=datetime.now)
    type: str  # email, linkedin_message, phone_call, coffee, event
    notes: str
    sentiment: str = "neutral"  # positive, neutral, negative
    follow_up_needed: bool = False
    follow_up_date: Optional[datetime] = None

class UserProfile(BaseModel):
    id: Optional[int] = None
    name: str
    email: EmailStr
    linkedin_profile: Optional[str] = None
    career_goals: Optional[str] = None
    target_industries: Optional[List[str]] = None
    created_at: datetime = Field(default_factory=datetime.now)

# Request/Response models for new endpoints
class PrioritizeRequest(BaseModel):
    contacts: List[Contact]
    interactions: Optional[List[Interaction]] = None
    limit: Optional[int] = None

class ScheduleRequest(BaseModel):
    contacts: List[Contact]
    interactions: Optional[List[Interaction]] = None
    contacts_per_week: int = 5

class MessageRequest(BaseModel):
    contact_name: str
    company: str
    context: str = ""

class NetworkAnalysisRequest(BaseModel):
    total_contacts: int
    active_contacts: int
EOF
