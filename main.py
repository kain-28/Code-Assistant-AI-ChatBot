from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional
import uvicorn

from env_config import load_backend_env

load_backend_env()

app = FastAPI(title="KAIN API", description="Backend for KAIN Coding Assistant")

# CORS Configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

from llm_service import llm_service
from rag_service import rag_service

class Message(BaseModel):
    role: str
    content: str

class ChatRequest(BaseModel):
    messages: List[Message]
    stream: Optional[bool] = False

@app.get("/")
async def root():
    return {"message": "KAIN API is running", "status": "healthy"}

@app.post("/api/chat")
async def chat(request: ChatRequest):
    try:
        # Get the last user message
        user_query = request.messages[-1].content
        
        # Retrieve context using RAG
        context = rag_service.search(user_query)
        
        # Get response from LLM
        response_text = await llm_service.get_response(request.messages, context=context)
        
        return {"response": response_text}
    except Exception as e:
        print(f"Error in chat endpoint: {e}")
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
