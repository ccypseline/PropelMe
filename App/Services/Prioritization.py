mkdir -p App/services
touch App/services/__init__.py

cat > App/services/prioritization.py << 'EOF'
from typing import List, Dict
from datetime import datetime, timedelta
from ..Schemas import Contact, Interaction, RelationshipType

class ContactPrioritization:
    """Advanced contact prioritization algorithm"""
    
    # Relationship strength weights
    RELATIONSHIP_WEIGHTS = {
        RelationshipType.CLOSE_FRIEND: 25,
        RelationshipType.FRIEND: 20,
        RelationshipType.CURRENT_COLLEAGUE: 18,
        RelationshipType.FORMER_COLLEAGUE: 15,
        RelationshipType.ACQUAINTANCE: 10,
        RelationshipType.MET_ONCE: 5,
        RelationshipType.NEVER_MET: 2
    }
    
    def calculate_priority_score(
        self, 
        contact: Contact, 
        interactions: List[Interaction] = None
    ) -> float:
        """Calculate comprehensive priority score (0-100)"""
        
        score = 0.0
        
        # 1. Recency Score (40 points max)
        score += self._calculate_recency_score(contact)
        
        # 2. Relationship Strength (25 points max)
        score += self.RELATIONSHIP_WEIGHTS.get(contact.relationship, 10)
        
        # 3. Interaction Frequency (20 points max)
        if interactions:
            score += self._calculate_frequency_score(contact, interactions)
        
        # 4. Warmth/Quality Score (15 points max)
        score += (contact.warmth_score / 100) * 15
        
        return min(100.0, score)
    
    def _calculate_recency_score(self, contact: Contact) -> float:
        """Score based on time since last interaction (higher = more stale = higher priority)"""
        
        if not contact.last_interaction_date:
            return 40.0  # Never contacted = highest priority
        
        days_since = (datetime.now() - contact.last_interaction_date).days
        
        if days_since < 30:
            return 5.0  # Recent, low priority
        elif days_since < 60:
            return 15.0
        elif days_since < 90:
            return 25.0
        elif days_since < 180:
            return 35.0
        else:
            return 40.0  # Very stale, high priority
    
    def _calculate_frequency_score(
        self, 
        contact: Contact, 
        interactions: List[Interaction]
    ) -> float:
        """Score based on interaction frequency in last year"""
        
        # Count interactions in last 365 days
        one_year_ago = datetime.now() - timedelta(days=365)
        recent_interactions = [
            i for i in interactions 
            if i.contact_id == contact.id and i.date > one_year_ago
        ]
        
        count = len(recent_interactions)
        
        if count == 0:
            return 20.0  # No recent interactions = high priority
        elif count < 3:
            return 15.0
        elif count < 6:
            return 10.0
        elif count < 12:
            return 5.0
        else:
            return 2.0  # Very frequent contact = low priority
    
    def prioritize_contacts(
        self, 
        contacts: List[Contact], 
        interactions: List[Interaction] = None,
        limit: int = None
    ) -> List[Contact]:
        """Sort contacts by priority score"""
        
        # Calculate scores
        for contact in contacts:
            contact.priority_score = self.calculate_priority_score(
                contact, 
                interactions
            )
        
        # Sort by priority (highest first)
        sorted_contacts = sorted(
            contacts, 
            key=lambda c: c.priority_score, 
            reverse=True
        )
        
        if limit:
            return sorted_contacts[:limit]
        
        return sorted_contacts
    
    def generate_outreach_schedule(
        self, 
        contacts: List[Contact],
        interactions: List[Interaction] = None,
        contacts_per_week: int = 5
    ) -> Dict[str, List[Contact]]:
        """Generate weekly outreach schedule"""
        
        # Prioritize contacts
        prioritized = self.prioritize_contacts(contacts, interactions)
        
        # Group into weeks
        schedule = {}
        current_date = datetime.now()
        
        for i, contact in enumerate(prioritized):
            week_num = i // contacts_per_week
            week_start = current_date + timedelta(weeks=week_num)
            week_key = week_start.strftime("%Y-W%W")
            
            if week_key not in schedule:
                schedule[week_key] = []
            
            schedule[week_key].append(contact)
        
        return schedule
    
    def calculate_warmth_score(
        self, 
        contact: Contact, 
        interactions: List[Interaction]
    ) -> float:
        """Calculate relationship warmth based on interaction quality"""
        
        if not interactions:
            return 50.0  # Neutral baseline
        
        # Get recent interactions
        six_months_ago = datetime.now() - timedelta(days=180)
        recent = [
            i for i in interactions 
            if i.contact_id == contact.id and i.date > six_months_ago
        ]
        
        if not recent:
            return 40.0  # Slightly cold
        
        # Quality weights
        sentiment_scores = {
            "positive": 10,
            "neutral": 5,
            "negative": -5
        }
        
        type_scores = {
            "coffee": 15,
            "phone_call": 12,
            "event": 10,
            "linkedin_message": 7,
            "email": 5
        }
        
        total_score = 50.0  # Start at neutral
        
        for interaction in recent[:10]:  # Last 10 interactions
            total_score += sentiment_scores.get(interaction.sentiment, 0)
            total_score += type_scores.get(interaction.type, 5)
        
        # Normalize to 0-100
        return max(0.0, min(100.0, total_score))
EOF
