cat > App/Routers/Contacts.py << 'EOF'
from fastapi import APIRouter, HTTPException
from typing import List, Optional
from pydantic import BaseModel
from ..Schemas import Contact, Interaction
from ..services.prioritization import ContactPrioritization

router = APIRouter(prefix="/contacts", tags=["Contact Management"])

prioritizer = ContactPrioritization()

class PrioritizeRequest(BaseModel):
    contacts: List[Contact]
    interactions: Optional[List[Interaction]] = None
    limit: Optional[int] = None

class ScheduleRequest(BaseModel):
    contacts: List[Contact]
    interactions: Optional[List[Interaction]] = None
    contacts_per_week: int = 5

@router.post("/prioritize")
async def prioritize_contacts(request: PrioritizeRequest):
    """Prioritize contacts for outreach"""
    try:
        prioritized = prioritizer.prioritize_contacts(
            request.contacts,
            request.interactions,
            request.limit
        )
        
        return {
            "status": "success",
            "total_contacts": len(request.contacts),
            "prioritized_contacts": [c.dict() for c in prioritized]
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/schedule")
async def generate_schedule(request: ScheduleRequest):
    """Generate weekly outreach schedule"""
    try:
        schedule = prioritizer.generate_outreach_schedule(
            request.contacts,
            request.interactions,
            request.contacts_per_week
        )
        
        # Convert to serializable format
        schedule_dict = {
            week: [c.dict() for c in contacts]
            for week, contacts in schedule.items()
        }
        
        return {
            "status": "success",
            "weeks": len(schedule),
            "schedule": schedule_dict
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/calculate-warmth")
async def calculate_warmth(contact: Contact, interactions: List[Interaction]):
    """Calculate relationship warmth score"""
    try:
        warmth = prioritizer.calculate_warmth_score(contact, interactions)
        
        return {
            "status": "success",
            "contact": contact.name,
            "warmth_score": warmth
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
EOF
