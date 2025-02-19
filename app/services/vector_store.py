from typing import List, Optional
import os
import faiss
import numpy as np
from langchain_openai import OpenAIEmbeddings
from langchain_community.docstore.in_memory import InMemoryDocstore
from langchain_community.vectorstores import FAISS
from app.core.config import get_settings

settings = get_settings()

class VectorStoreService:
    def __init__(self):
        self.embeddings = OpenAIEmbeddings(
            openai_api_key=settings.OPENAI_API_KEY
        )
        self.vector_store = self._load_or_create_store()

    def _load_or_create_store(self) -> FAISS:
        """Load existing FAISS index or create a new one"""
        if os.path.exists(settings.FAISS_INDEX_PATH):
            return FAISS.load_local(
                settings.FAISS_INDEX_PATH,
                self.embeddings,
                allow_dangerous_deserialization=True
            )
        
        # Create new vector store
        vector_store = FAISS.from_texts(
            [""], 
            self.embeddings,
            docstore=InMemoryDocstore({})
        )
        # Ensure directory exists
        os.makedirs(os.path.dirname(settings.FAISS_INDEX_PATH), exist_ok=True)
        vector_store.save_local(settings.FAISS_INDEX_PATH)
        return vector_store

    async def similarity_search(self, query: str, k: int = 4) -> List[dict]:
        """Search for similar documents"""
        try:
            return self.vector_store.similarity_search(query, k=k)
        except Exception as e:
            if "index does not exist" in str(e).lower():
                raise Exception("No documents have been indexed yet")
            raise e

    async def add_texts(self, texts: List[str], metadatas: Optional[List[dict]] = None) -> List[str]:
        """Add texts to the vector store"""
        try:
            ids = self.vector_store.add_texts(texts, metadatas)
            self.vector_store.save_local(settings.FAISS_INDEX_PATH)
            return ids
        except Exception as e:
            raise Exception(f"Error adding texts to vector store: {str(e)}") 