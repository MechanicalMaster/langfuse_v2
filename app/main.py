from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse, JSONResponse
from .core.config import get_settings
from .api import chat, documents
import os
from datetime import datetime

settings = get_settings()

app = FastAPI(title=settings.PROJECT_NAME)

# Configure CORS with more specific settings
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.BACKEND_CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE"],
    allow_headers=["*"],
    max_age=86400,  # 24 hours
)

# Mount static files
app.mount("/static", StaticFiles(directory="app/static"), name="static")

# Add routers
app.include_router(chat.router, prefix=f"{settings.API_V1_STR}/chat", tags=["chat"])
app.include_router(documents.router, prefix=f"{settings.API_V1_STR}/documents", tags=["documents"])

@app.get("/")
async def root():
    return FileResponse("app/static/index.html")

@app.get("/health")
async def health_check():
    """Simple health check endpoint for Railway"""
    return JSONResponse(
        content={
            "status": "healthy",
            "timestamp": datetime.utcnow().isoformat(),
            "version": "1.0.0"
        },
        status_code=200
    ) 