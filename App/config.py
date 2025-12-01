cat > App/config.py << 'EOF'
import os

class Settings:
    # App
    app_name: str = "PropelMe"
    environment: str = os.getenv("ENVIRONMENT", "production")
    
    # Google Cloud & Vertex AI
    google_project_id: str = os.getenv("GOOGLE_PROJECT_ID", "")
    gcp_region: str = "us-central1"
    gemini_model: str = "gemini-2.0-flash-exp"
    
    # LinkedIn OAuth
    linkedin_client_id: str | None = os.getenv("LINKEDIN_CLIENT_ID")
    linkedin_client_secret: str | None = os.getenv("LINKEDIN_CLIENT_SECRET")
    linkedin_redirect_uri: str = os.getenv(
        "LINKEDIN_REDIRECT_URI",
        "https://propelme-backend-409735787031.us-central1.run.app/auth/linkedin/callback"
    )
    
    # Eventbrite
    eventbrite_api_key: str | None = os.getenv("EVENTBRITE_API_KEY")
    
    def validate(self):
        if not self.google_project_id:
            raise ValueError("GOOGLE_PROJECT_ID required")
    
    def has_linkedin(self) -> bool:
        return bool(self.linkedin_client_id and self.linkedin_client_secret)
    
    def has_eventbrite(self) -> bool:
        return bool(self.eventbrite_api_key)

settings = Settings()
EOF
