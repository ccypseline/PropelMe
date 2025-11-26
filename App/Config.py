import os

class Settings:
    # App basics
    app_name: str = "PropelMe"
    environment: str = os.getenv("ENVIRONMENT", "production")
    
    # Google Cloud - reads from environment variable
    google_project_id: str = os.getenv("GOOGLE_PROJECT_ID", "")
    gcp_region: str = "us-central1"
    
    # Gemini settings
    gemini_model: str = "gemini-2.0-flash-exp"
    
    # Firebase - reads from environment variables
    firebase_project_id: str | None = os.getenv("FIREBASE_PROJECT_ID")
    firebase_client_email: str | None = os.getenv("FIREBASE_CLIENT_EMAIL")
    firebase_private_key: str | None = os.getenv("FIREBASE_PRIVATE_KEY")
    
    # Database
    db_connection_url: str | None = os.getenv("DB_CONNECTION_URL")
    
    def validate(self):
        if not self.google_project_id:
            raise ValueError("GOOGLE_PROJECT_ID is required!")

settings = Settings()
