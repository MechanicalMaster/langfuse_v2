from typing import BinaryIO, List
from pathlib import Path
import os
from fastapi import UploadFile, HTTPException
from app.core.config import get_settings
from app.services.vector_store import VectorStoreService
from langfuse.client import Langfuse
import time
from app.core.observability import langfuse

settings = get_settings()

class DocumentService:
    def __init__(self):
        self.vector_store = VectorStoreService()

    def _validate_file(self, file: UploadFile) -> None:
        """Validate file type and size"""
        # Check file extension
        file_ext = Path(file.filename).suffix.lower()
        if file_ext not in settings.ALLOWED_FILE_TYPES:
            raise HTTPException(
                status_code=400,
                detail=f"File type not allowed. Allowed types: {settings.ALLOWED_FILE_TYPES}"
            )

        # Check file size
        file.file.seek(0, os.SEEK_END)
        file_size = file.file.tell()
        file.file.seek(0)
        
        if file_size > settings.MAX_FILE_SIZE:
            raise HTTPException(
                status_code=400,
                detail=f"File too large. Maximum size: {settings.MAX_FILE_SIZE/1024}KB"
            )

    async def process_document(self, text: str, filename: str):
        """Process a document and store it in the vector store"""
        try:
            # Create trace
            trace = langfuse.trace(
                name="document_processing",
                id=filename,  # Use filename as trace ID
                metadata={
                    "filename": filename,
                    "file_size": len(text)
                }
            )

            try:
                start_time = time.time()
                
                # Process chunks
                chunks = text.split('\n\n')
                chunks = [chunk.strip() for chunk in chunks if chunk.strip()]

                # Add metadata to chunks
                metadatas = [{"source": filename, "chunk": i} for i in range(len(chunks))]
                
                # Store in vector store
                await self.vector_store.add_texts(chunks, metadatas)

                duration = time.time() - start_time

                # Update trace with success
                trace.update(
                    metadata={
                        "chunks_processed": len(chunks),
                        "avg_chunk_size": sum(len(c) for c in chunks) / len(chunks) if chunks else 0,
                        "duration": duration
                    },
                    status="success"
                )

                return {
                    "filename": filename,
                    "chunks_processed": len(chunks)
                }

            except Exception as e:
                trace.update(
                    metadata={"error": str(e)},
                    status="error"
                )
                raise e

        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))

    async def process_document_file(self, file: UploadFile) -> dict:
        """Process uploaded document and store in vector store"""
        try:
            self._validate_file(file)
            
            # Read and decode content
            content = await file.read()
            text = content.decode('utf-8')
            
            # Split text into chunks (simple splitting by paragraphs for now)
            chunks = [chunk.strip() for chunk in text.split('\n\n') if chunk.strip()]
            
            # Add metadata to each chunk
            metadatas = [{"source": file.filename, "chunk_index": i} for i in range(len(chunks))]
            
            # Store in vector store
            await self.vector_store.add_texts(chunks, metadatas)
            
            return {
                "message": "Document processed successfully",
                "filename": file.filename,
                "chunks_processed": len(chunks)
            }
            
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e)) 