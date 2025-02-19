from fastapi import APIRouter, Depends, HTTPException
from app.services.chat_service import ChatService
from .models import ChatRequest

router = APIRouter()

@router.post("/chat")
async def chat(
    request: ChatRequest,
    chat_service: ChatService = Depends(lambda: ChatService())
):
    try:
        response = await chat_service.chat(request.message, request.session_id)
        return {"response": response}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e)) 