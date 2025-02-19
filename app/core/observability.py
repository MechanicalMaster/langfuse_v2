from langfuse.client import Langfuse
from app.core.config import get_settings

settings = get_settings()

# Create shared Langfuse client
langfuse = Langfuse(
    public_key=settings.LANGFUSE_PUBLIC_KEY,
    secret_key=settings.LANGFUSE_SECRET_KEY,
    host="https://us.cloud.langfuse.com"
) 