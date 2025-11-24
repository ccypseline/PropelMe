import os
from functools import lru_cache

class Settings:
    app_name: str = "PropelMe Backend"
    environment: str = os.getenv("ENVIRONMENT", "local")
    db_connection_url: str | None = os.getenv("DB_CONNECTION_URL")

    # Firebase
    firebase_project_id: str | None = os.getenv("FIREBASE_PROJECT_ID")
    firebase_client_email: str | None = os.getenv("FIREBASE_CLIENT_EMAIL")
    firebase_private_key: str | None = os.getenv("FIREBASE_PRIVATE_KEY")

@lru_cache
def get_settings() -> Settings:
    return Settings()
