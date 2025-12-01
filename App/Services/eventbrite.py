cat > app/services/eventbrite.py << 'EOF'
from typing import List, Dict, Optional
import httpx
from datetime import datetime
from ..Config import settings

class EventbriteService:
    """Eventbrite API integration for networking events"""
    
    BASE_URL = "https://www.eventbriteapi.com/v3"
    
    def __init__(self, api_key: Optional[str] = None):
        self.api_key = api_key or settings.eventbrite_api_key
    
    def _get_headers(self) -> Dict:
        if not self.api_key:
            raise ValueError("Eventbrite API key not configured")
        
        return {"Authorization": f"Bearer {self.api_key}"}
    
    async def search_events(
        self,
        keywords: str = "networking",
        location: Optional[str] = None,
        categories: List[str] = None,
        start_date: Optional[datetime] = None,
        page: int = 1
    ) -> Dict:
        """Search for networking events"""
        
        params = {
            "q": keywords,
            "page": page,
            "expand": "venue,organizer"
        }
        
        if location:
            params["location.address"] = location
        
        # Eventbrite categories: 101=Business, 103=Networking
        if categories:
            params["categories"] = ",".join(categories)
        else:
            params["categories"] = "101,103"
        
        if start_date:
            params["start_date.range_start"] = start_date.isoformat()
        
        async with httpx.AsyncClient() as client:
            response = await client.get(
                f"{self.BASE_URL}/events/search/",
                headers=self._get_headers(),
                params=params,
                timeout=10.0
            )
            
            if response.status_code != 200:
                return {
                    "error": f"Eventbrite API error: {response.status_code}",
                    "events": []
                }
            
            data = response.json()
            
            return {
                "total": data.get("pagination", {}).get("object_count", 0),
                "events": [self._parse_event(e) for e in data.get("events", [])]
            }
    
    async def get_event_details(self, event_id: str) -> Dict:
        """Get detailed information about a specific event"""
        
        async with httpx.AsyncClient() as client:
            response = await client.get(
                f"{self.BASE_URL}/events/{event_id}/",
                headers=self._get_headers(),
                params={"expand": "venue,organizer,ticket_classes"},
                timeout=10.0
            )
            
            if response.status_code != 200:
                return {"error": f"Event not found: {event_id}"}
            
            return self._parse_event(response.json())
    
    async def get_event_attendees(self, event_id: str) -> List[Dict]:
        """Get attendees for an event (requires organizer access)"""
        
        async with httpx.AsyncClient() as client:
            response = await client.get(
                f"{self.BASE_URL}/events/{event_id}/attendees/",
                headers=self._get_headers(),
                timeout=10.0
            )
            
            if response.status_code != 200:
                return []
            
            data = response.json()
            return data.get("attendees", [])
    
    def _parse_event(self, event_data: Dict) -> Dict:
        """Parse Eventbrite event data into simplified format"""
        
        venue = event_data.get("venue", {})
        organizer = event_data.get("organizer", {})
        
        return {
            "id": event_data.get("id"),
            "name": event_data.get("name", {}).get("text"),
            "description": event_data.get("description", {}).get("text", "")[:500],
            "url": event_data.get("url"),
            "start": event_data.get("start", {}).get("local"),
            "end": event_data.get("end", {}).get("local"),
            "is_online": event_data.get("online_event", False),
            "venue": {
                "name": venue.get("name"),
                "address": venue.get("address", {}).get("localized_address_display"),
                "city": venue.get("address", {}).get("city"),
                "latitude": venue.get("latitude"),
                "longitude": venue.get("longitude")
            },
            "organizer": {
                "name": organizer.get("name"),
                "description": organizer.get("description", {}).get("text", "")[:200]
            },
            "capacity": event_data.get("capacity"),
            "is_free": event_data.get("is_free", False),
            "logo_url": event_data.get("logo", {}).get("url")
        }
EOF
