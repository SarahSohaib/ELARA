from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Optional

from models import RecommendationRequest, RecommendationResponse, RecommendedItem, IngestionRequest, FeedbackRequest
from embeddings import Embedder
from vector_db import vector_db
from llm_generator import LLMGenerator
from ingestion import DataIngestionService
from cache import query_cache
from feedback import feedback_manager
from metrics import app_metrics
import time

# Initialize subsystems
try:
    embedder = Embedder()
except Exception as e:
    print(f"Warning: Could not initialize embedder: {e}")
    embedder = None
llm_gen = LLMGenerator()
from fastapi import FastAPI
from backend.api.routes import router

app = FastAPI(title="ELARA")

app.include_router(router)

class ChatResponse(BaseModel):
    response: str

@app.post("/api/chat", response_model=ChatResponse)
def chat(request: ChatRequest):
    return {"response": "ELARA backend connected successfully"}

@app.post("/api/recommend", response_model=RecommendationResponse)
def recommend(request: RecommendationRequest):
    """
    Given a natural language context, returns explainable recommendations.
    Uses RAG: embeds the query -> searches vector DB -> generates explanation via LLM.
    Includes caching and performance metrics tracking.
    """
    start_time = time.time()
    
    # Check Cache First
    cached_data = query_cache.get(request.query)
    if cached_data:
        latency = (time.time() - start_time) * 1000
        app_metrics.record_query(latency, cache_hit=True)
        return RecommendationResponse(**cached_data)

    if not embedder:
        raise HTTPException(status_code=500, detail="Embedding model not initialized.")

    # Step 1: Embed Query
    query_emb = embedder.embed_query(request.query)

    # Step 2: Semantic Retrieval from FAISS DB
    try:
        retrieved_data = vector_db.search(query_emb, top_k=request.top_k)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Database search failed: {str(e)}")

    if not retrieved_data:
        return RecommendationResponse(
            query=request.query,
            recommendations=[],
            explanation="No relevant items found."
        )

    # Step 3: LLM generation for explainability
    explanation = llm_gen.generate_explanation(request.query, retrieved_data)

    # Format the response
    recommendations = [
        RecommendedItem(
            id=item["id"],
            title=item["title"],
            description=item["description"],
            score=item["score"]
        ) for item in retrieved_data
    ]

    response_data = {
        "query": request.query,
        "recommendations": recommendations,
        "explanation": explanation,
        "cache_hit": False
    }

    # Store in Cache
    query_cache.set(request.query, response_data)

    # Record Metrics
    latency = (time.time() - start_time) * 1000
    app_metrics.record_query(latency, cache_hit=False)

    return RecommendationResponse(**response_data)

@app.post("/api/ingest")
def ingest_data(request: IngestionRequest):
    """
    Dynamically add new items securely into the vector database.
    """
    if not embedder:
        raise HTTPException(status_code=500, detail="Embedder not initialized.")
    
    ingest_svc = DataIngestionService(embedder)
    items_dicts = [{"title": i.title, "description": i.description} for i in request.items]
    
    result = ingest_svc.ingest_items(items_dicts)
    if result["status"] == "error":
        raise HTTPException(status_code=400, detail=result["message"])
        
    # Clear cache since DB changed
    query_cache.clear()
    return result

@app.post("/api/feedback")
def submit_feedback(request: FeedbackRequest):
    """
    Collect user feedback (1-5 rating) on a specific recommendation.
    """
    try:
        feedback_manager.record_feedback(request.query, request.rating, request.comments)
        return {"status": "success", "message": "Feedback recorded"}
    except ValueError as val_err:
         raise HTTPException(status_code=400, detail=str(val_err))
    except Exception as e:
         raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/metrics")
def get_system_metrics():
    """
    Returns system performance and user feedback analytics.
    """
    metrics = app_metrics.get_metrics()
    metrics["average_feedback_rating"] = feedback_manager.get_average_rating()
    metrics["total_feedback_received"] = len(feedback_manager.get_all_feedback())
    return metrics

@app.get("/")
def root():
    return {"message": "ELARA backend running"}
