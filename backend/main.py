from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import time
from fastapi.middleware.cors import CORSMiddleware


# ✅ FIXED IMPORTS (direct, no __init__ dependency)
from backend.models.query_model import QueryRequest

# (Keep others ONLY if they exist properly, else comment for now)
# from backend.models.response_model import RecommendationResponse, RecommendedItem
# from backend.models.other_models import IngestionRequest, FeedbackRequest, ChatRequest, HealthResponse

from backend.embeddings import Embedder
from backend.vector_db import vector_db
from backend.llm_generator import LLMGenerator
from backend.ingestion import DataIngestionService
from backend.cache import query_cache
from backend.feedback import feedback_manager
from backend.metrics import app_metrics

from backend.api.routes import router

# Initialize FastAPI
app = FastAPI(title="ELARA")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # allow frontend
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routes
#app.include_router(router)

# Initialize subsystems
try:
    embedder = Embedder()
except Exception as e:
    print(f"Warning: Could not initialize embedder: {e}")
    embedder = None

llm_gen = LLMGenerator()


# ✅ SIMPLE TEST ENDPOINT
@app.get("/")
def root():
    return {"message": "ELARA backend running"}


# ✅ TEMP CHAT MODEL (so it runs)
class ChatRequest(BaseModel):
    message: str


class ChatResponse(BaseModel):
    response: str


@app.post("/api/chat", response_model=ChatResponse)
def chat(request: ChatRequest):
    return {"response": f"Echo: {request.message}"}

@app.post("/api/recommend")
def recommend(request: QueryRequest):
    return {
        "query": request.query,
        "recommendations": [
            {
                "id": 1,
                "title": "Inception",
                "type": "Movie",
                "year": 2010,
                "tags": ["Sci-Fi", "Thriller"],
                "score": 95,
                "explanation": f"Recommended based on your query: {request.query}"
            }
        ]
    }