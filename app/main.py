from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse, JSONResponse
from .core.config import get_settings
from .api import chat, documents
import os
from datetime import datetime

settings = get_settings()

app = FastAPI(
    title=settings.PROJECT_NAME,
    docs_url=None if os.getenv("RAILWAY_ENVIRONMENT") else "/docs",
    redoc_url=None if os.getenv("RAILWAY_ENVIRONMENT") else "/redoc"
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Temporarily allow all origins for testing
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Basic routes first
@app.get("/health")
async def health_check():
    """Basic health check endpoint"""
    return {"status": "ok"}

@app.get("/")
async def root():
    """Serve the static index.html"""
    try:
        return FileResponse("app/static/index.html")
    except Exception as e:
        return JSONResponse(
            content={"message": "Welcome to Policy Chatbot API"},
            status_code=200
        )

# Mount static files after basic routes
app.mount("/static", StaticFiles(directory="app/static"), name="static")

# Add API routers last
app.include_router(chat.router, prefix=f"{settings.API_V1_STR}/chat", tags=["chat"])
app.include_router(documents.router, prefix=f"{settings.API_V1_STR}/documents", tags=["documents"]) 