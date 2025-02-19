from typing import Dict, List
from langchain_openai import ChatOpenAI
from langchain.prompts import ChatPromptTemplate
from langgraph.graph import StateGraph
from langchain.schema import BaseMessage, HumanMessage, AIMessage
from app.services.vector_store import VectorStoreService
from app.core.observability import langfuse
from fastapi import HTTPException
import time

from app.core.config import get_settings

settings = get_settings()

class ChatService:
    def __init__(self):
        self.llm = ChatOpenAI(
            temperature=0,
            openai_api_key=settings.OPENAI_API_KEY
        )
        self.vector_store = VectorStoreService()
        self.conversation_states: Dict[str, List[BaseMessage]] = {}

    async def _retrieve_context(self, query: str) -> str:
        """Retrieve relevant context from vector store"""
        try:
            docs = await self.vector_store.similarity_search(query)
            if not docs:
                return "No relevant policy information found. Please try another question or upload a policy document first."
            return "\n".join([doc.page_content for doc in docs])
        except Exception as e:
            if "index does not exist" in str(e).lower():
                return "No policy documents have been uploaded yet. Please upload a document first."
            raise e

    async def chat(self, message: str, session_id: str) -> str:
        """Process a chat message and return the response"""
        try:
            # Initialize conversation state if needed
            if session_id not in self.conversation_states:
                self.conversation_states[session_id] = []

            # Add user message to state
            self.conversation_states[session_id].append(HumanMessage(content=message))

            # Retrieve context
            context = await self._retrieve_context(message)

            # Create trace
            trace = langfuse.trace(
                name="chat_interaction",
                id=session_id,  # Added session_id as trace ID
                metadata={
                    "session_id": session_id,
                    "message_length": len(message),
                    "context_length": len(context)
                }
            )

            try:
                # Create and use prompt
                prompt = ChatPromptTemplate.from_messages([
                    ("system", """You are a helpful assistant that answers questions based on the provided policy documents. 
                    If no relevant information is found in the context, politely explain that to the user.
                    
                    Context: {context}"""),
                    ("human", "{question}")
                ])

                # Log generation
                generation = trace.generation(
                    name="chat_response",
                    model="gpt-3.5-turbo",
                    parameters={"temperature": 0},
                    input={
                        "message": message,
                        "context": context
                    }
                )

                # Get response from LLM
                start_time = time.time()
                chain = prompt | self.llm
                response = await chain.ainvoke({
                    "context": context,
                    "question": message
                })
                duration = time.time() - start_time

                # Update generation with result
                generation.update(
                    output=response.content,
                    metadata={
                        "response_length": len(response.content),
                        "duration": duration
                    }
                )

                # Add AI response to state
                self.conversation_states[session_id].append(AIMessage(content=response.content))
                
                return response.content

            except Exception as e:
                if 'generation' in locals():
                    generation.update(
                        metadata={"error": str(e)},
                        status="error"
                    )
                raise e

        except Exception as e:
            if 'trace' in locals():
                trace.update(
                    metadata={"error": str(e)},
                    status="error"
                )
            raise HTTPException(
                status_code=500,
                detail=f"Error processing chat message: {str(e)}"
            ) 