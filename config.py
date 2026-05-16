import os
from typing import Optional

class Settings:
    ENV = os.getenv("ENVIRONMENT", "development").lower()
    DEBUG = ENV == "development"
    
    # Firebase
    FIREBASE_KEY_PATH = os.getenv("FIREBASE_KEY_PATH", "serviceAccountKey.json")
    FIREBASE_KEY_JSON = os.getenv("FIREBASE_KEY_JSON")
    
    # Database
    DATABASE_NAME = "development" if ENV == "development" else "production"
    
    # API
    API_URL = os.getenv("API_URL", "http://localhost:8000")
    
    
    # CORS
    ALLOWED_ORIGINS = os.getenv("ALLOWED_ORIGINS", "http://localhost:3000").split(",")

settings = Settings()

