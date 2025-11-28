cat > App/Routers/Contacts.py << 'EOF'
from fastapi import APIRouter, HTTPException
from typing import List, Optional
from ..Schemas import Contact, Interaction, PrioritizeRequest, ScheduleRequest
from ..services.prioritization import ContactPrioritization

router = APIRouter(prefix="/contacts", tags=["Contact Management"])

prioritizer = ContactPrioritization()

@router.post("/prioritize")
async def prioritize_contacts(request: PrioritizeRequest):
    """Prioritize contacts for outreach using smart scoring"""
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
            "total_contacts": len(request.contacts),
            "schedule": schedule_dict
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/calculate-warmth")
async def calculate_warmth(contact: Contact, interactions: List[Interaction]):
    """Calculate relationship warmth score for a contact"""
    try:
        warmth = prioritizer.calculate_warmth_score(contact, interactions)
        
        # Update warmth bucket
        if warmth >= 70:
            bucket = "hot"
        elif warmth >= 40:
            bucket = "warm"
        else:
            bucket = "cold"
        
        return {
            "status": "success",
            "contact": contact.name,
            "warmth_score": warmth,
            "warmth_bucket": bucket
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
EOF
