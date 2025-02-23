from pydantic_settings import BaseSettings
from functools import lru_cache
from typing import List

class Settings(BaseSettings):
    PROJECT_NAME: str = "Policy Chatbot"
    API_V1_STR: str = "/api/v1"
    
    # Authentication
    AUTH_PASSWORD: str = "Langfuse"
    
    # OpenAI (required)
    OPENAI_API_KEY: str
    
    # Langfuse (optional)
    LANGFUSE_PUBLIC_KEY: str = ""
    LANGFUSE_SECRET_KEY: str = ""
    
    # CORS
    BACKEND_CORS_ORIGINS: List[str] = ["*"]
    
    # File Upload
    MAX_FILE_SIZE: int = 25 * 1024
    ALLOWED_FILE_TYPES: set[str] = {".txt"}
    
    # Vector Store
    FAISS_INDEX_PATH: str = "/tmp/faiss_index"  # Use /tmp for Railway's ephemeral storage
    
    class Config:
        env_file = ".env"

@lru_cache()
def get_settings():
    return Settings() 