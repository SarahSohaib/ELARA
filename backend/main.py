from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI(title="ELARA Backend")

class ChatRequest(BaseModel):
    message: str

class ChatResponse(BaseModel):
    response: str

@app.post("/api/chat", response_model=ChatResponse)
def chat(request: ChatRequest):
    return {"response": "ELARA backend connected successfully"}
