from fastapi import APIRouter, Depends, HTTPException, UploadFile, File
from app.services.document_service import DocumentService

router = APIRouter()

@router.post("/upload")
async def upload_document(
    file: UploadFile = File(...),
    document_service: DocumentService = Depends(lambda: DocumentService())
):
    try:
        content = await file.read()
        text = content.decode('utf-8')
        result = await document_service.process_document(text, file.filename)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e)) 