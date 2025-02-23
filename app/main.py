from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from .core.config import get_settings
from .api import chat, documents

settings = get_settings()

app = FastAPI(title=settings.PROJECT_NAME)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.BACKEND_CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount static files
# Mount static files
static_dir = "app/static"
if os.path.exists(static_dir):
    app.mount("/static", StaticFiles(directory=static_dir), name="static")

# Add routers
app.include_router(chat.router, prefix=f"{settings.API_V1_STR}/chat", tags=["chat"])
app.include_router(documents.router, prefix=f"{settings.API_V1_STR}/documents", tags=["documents"])

@app.get("/health")
async def health_check():
    """Health check endpoint for Railway"""
    try:
        status_checks = {
            "base_api": "healthy",
            "environment": "production" if os.getenv("RAILWAY_ENVIRONMENT") else "development"
        }
        
        # Optional Langfuse check
        try:
            langfuse.trace(name="health_check")
            status_checks["langfuse"] = "connected"
        except Exception as e:
            status_checks["langfuse"] = "disconnected"
            
        return {
            "status": "healthy",
            "checks": status_checks,
            "timestamp": datetime.utcnow().isoformat()
        }
    except Exception as e:
        return {
            "status": "unhealthy",
            "error": str(e),
            "timestamp": datetime.utcnow().isoformat()
        }