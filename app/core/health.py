from typing import Dict, Any
from datetime import datetime
import os

def check_environment() -> Dict[str, Any]:
    """Check if all required environment variables are set"""
    required_vars = [
        "OPENAI_API_KEY",
        "LANGFUSE_PUBLIC_KEY",
        "LANGFUSE_SECRET_KEY"
    ]
    
    missing_vars = [var for var in required_vars if not os.getenv(var)]
    
    return {
        "environment_ready": len(missing_vars) == 0,
        "missing_variables": missing_vars if missing_vars else None,
        "environment": os.getenv("RAILWAY_ENVIRONMENT", "development")
    }

def get_health_status() -> Dict[str, Any]:
    """Get complete health status"""
    env_status = check_environment()
    
    return {
        "status": "healthy" if env_status["environment_ready"] else "unhealthy",
        "timestamp": datetime.utcnow().isoformat(),
        "version": "1.0.0",
        "environment_status": env_status
    } 