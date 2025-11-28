cat > App/Routers/AI.py << 'EOF'
from fastapi import APIRouter, HTTPException
from ..agents.gemini_agent import GeminiAgent
from ..Config import settings
from ..Schemas import MessageRequest, NetworkAnalysisRequest

router = APIRouter(prefix="/ai", tags=["AI Networking"])

_agent = None

def get_agent():
    global _agent
    if _agent is None:
        _agent = GeminiAgent(
            project_id=settings.google_project_id,
            location=settings.gcp_region,
            model=settings.gemini_model
        )
    return _agent

@router.post("/generate-message")
async def generate_message(request: MessageRequest):
    """Generate AI-powered networking message"""
    try:
        settings.validate()
        agent = get_agent()
        message = agent.generate_message(
            request.contact_name,
            request.company,
            request.context
        )
        return {
            "status": "success",
            "message": message,
            "contact": request.contact_name
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/analyze-network")
async def analyze_network(request: NetworkAnalysisRequest):
    """Get AI network health analysis"""
    try:
        settings.validate()
        agent = get_agent()
        analysis = agent.analyze_network(
            request.total_contacts,
            request.active_contacts
        )
        return {
            "status": "success",
            "analysis": analysis,
            "total_contacts": request.total_contacts,
            "active_contacts": request.active_contacts
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
EOF
