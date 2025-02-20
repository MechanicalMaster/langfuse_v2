from pydantic_settings import BaseSettings
from functools import lru_cache
from typing import List
import os

class Settings(BaseSettings):
    PROJECT_NAME: str = "Policy Chatbot"
    API_V1_STR: str = "/api/v1"
    
    # Authentication
    AUTH_PASSWORD: str = os.getenv("AUTH_PASSWORD", "Langfuse")
    
    # OpenAI
    OPENAI_API_KEY: str = os.getenv("OPENAI_API_KEY", "")
    
    # Langfuse
    LANGFUSE_PUBLIC_KEY: str = os.getenv("LANGFUSE_PUBLIC_KEY", "")
    LANGFUSE_SECRET_KEY: str = os.getenv("LANGFUSE_SECRET_KEY", "")
    
    # CORS
    BACKEND_CORS_ORIGINS: List[str] = [
        "http://localhost",
        "http://localhost:8000",
        "https://localhost",
        "https://localhost:8000",
        "https://*.up.railway.app",
        "*"  # Allow all origins in development
    ]
    
    # File Upload
    MAX_FILE_SIZE: int = 25 * 1024  # 25KB
    ALLOWED_FILE_TYPES: set[str] = {".txt"}
    
    # Vector Store
    FAISS_INDEX_PATH: str = os.getenv("FAISS_INDEX_PATH", "data/faiss_index")
    
    class Config:
        env_file = ".env"

@lru_cache()
def get_settings():
    return Settings() 