from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import time
from fastapi.middleware.cors import CORSMiddleware
import sys
import os

# Add the current directory to Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# ✅ FIXED IMPORTS (direct, no __init__ dependency)
from models.query_model import QueryRequest

# (Keep others ONLY if they exist properly, else comment for now)
# from backend.models.response_model import RecommendationResponse, RecommendedItem
# from backend.models.other_models import IngestionRequest, FeedbackRequest, ChatRequest, HealthResponse

from embeddings import Embedder
from vector_db import vector_db
from llm_generator import LLMGenerator
from ingestion import DataIngestionService
from cache import query_cache
from feedback import feedback_manager
from metrics import app_metrics

from api.routes import router

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
app.include_router(router)

# Initialize subsystems
try:
    embedder = Embedder()
except Exception as e:
    print(f"Warning: Could not initialize embedder: {e}")
    embedder = None

llm_gen = LLMGenerator()

# Initialize data ingestion and load CSV data
data_ingestion = DataIngestionService(embedder)
if embedder:
    ingestion_result = data_ingestion.load_and_ingest_csv()
    print(f"Data ingestion result: {ingestion_result}")
else:
    print("Embedder not initialized, skipping data ingestion")


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