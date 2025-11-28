cat > App/Routers/Events.py << 'EOF'
from fastapi import APIRouter, HTTPException, Query
from typing import Optional, List
from datetime import datetime
from ..services.eventbrite import EventbriteService
from ..Config import settings

router = APIRouter(prefix="/events", tags=["Networking Events"])

@router.get("/search")
async def search_events(
    keywords: str = Query("networking", description="Search keywords"),
    location: Optional[str] = Query(None, description="City or address"),
    page: int = Query(1, ge=1, le=50)
):
    """Search for networking events on Eventbrite"""
    
    if not settings.has_eventbrite():
        raise HTTPException(
            status_code=501,
            detail="Eventbrite API not configured. Set EVENTBRITE_API_KEY environment variable."
        )
    
    try:
        service = EventbriteService()
        results = await service.search_events(
            keywords=keywords,
            location=location,
            page=page
        )
        
        return {
            "status": "success",
            "total": results.get("total", 0),
            "page": page,
            "events": results.get("events", [])
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/details/{event_id}")
async def get_event_details(event_id: str):
    """Get detailed information about a specific event"""
    
    if not settings.has_eventbrite():
        raise HTTPException(
            status_code=501,
            detail="Eventbrite API not configured"
        )
    
    try:
        service = EventbriteService()
        event = await service.get_event_details(event_id)
        
        if "error" in event:
            raise HTTPException(status_code=404, detail=event["error"])
        
        return {
            "status": "success",
            "event": event
        }
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/recommendations")
async def get_event_recommendations(
    location: Optional[str] = Query(None),
    interests: Optional[str] = Query("technology,business,professional development")
):
    """Get curated event recommendations for networking"""
    
    if not settings.has_eventbrite():
        return {
            "status": "info",
            "message": "Eventbrite API not configured. Configure it to get personalized event recommendations."
        }
    
    try:
        service = EventbriteService()
        
        # Search for multiple categories
        all_events = []
        for keyword in interests.split(","):
            results = await service.search_events(
                keywords=keyword.strip(),
                location=location
            )
            all_events.extend(results.get("events", []))
        
        # Remove duplicates
        seen_ids = set()
        unique_events = []
        for event in all_events:
            if event["id"] not in seen_ids:
                seen_ids.add(event["id"])
                unique_events.append(event)
        
        # Sort by date
        unique_events.sort(key=lambda e: e.get("start", ""))
        
        return {
            "status": "success",
            "total": len(unique_events),
            "events": unique_events[:20]  # Top 20
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
EOF
