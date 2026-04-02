# backend/main.py
import time
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Optional

from backend.models import (
    RecommendationRequest, RecommendationResponse,
    RecommendedItem, IngestionRequest, FeedbackRequest
)
from backend.embeddings import Embedder
from backend.vector_db import vector_db
from backend.llm_generator import LLMGenerator
from backend.ingestion import DataIngestionService
from backend.cache import query_cache
from backend.feedback import feedback_manager
from backend.metrics import app_metrics

app = FastAPI(title="ELARA")

# Initialize subsystems once at startup
try:
    embedder = Embedder()
    print("Embedder initialized successfully.")
except Exception as e:
    print(f"Warning: Could not initialize embedder: {e}")
    embedder = None

llm_gen = LLMGenerator()


class ChatRequest(BaseModel):
    message: str

class ChatResponse(BaseModel):
    response: str


@app.get("/")
def root():
    return {"message": "ELARA backend running"}


@app.post("/api/chat", response_model=ChatResponse)
def chat(request: ChatRequest):
    return {"response": "ELARA backend connected successfully"}


@app.post("/api/recommend", response_model=RecommendationResponse)
def recommend(request: RecommendationRequest):
    start_time = time.time()

    cached_data = query_cache.get(request.query)
    if cached_data:
        latency = (time.time() - start_time) * 1000
        app_metrics.record_query(latency, cache_hit=True)
        return RecommendationResponse(**cached_data)

    if not embedder:
        raise HTTPException(status_code=500, detail="Embedding model not initialized.")

    query_emb = embedder.embed_query(request.query)

    try:
        retrieved_data = vector_db.search(query_emb, top_k=request.top_k)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Database search failed: {str(e)}")

    if not retrieved_data:
        return RecommendationResponse(
            query=request.query,
            recommendations=[],
            explanation="No relevant items found.",
            cache_hit=False
        )

    explanation = llm_gen.generate_explanation(request.query, retrieved_data)

    recommendations = [
        RecommendedItem(
            id=item.get("id", str(i)),
            title=item["title"],
            description=item["description"],
            score=item["score"]
        ) for i, item in enumerate(retrieved_data)
    ]

    response_data = {
        "query": request.query,
        "recommendations": [r.dict() for r in recommendations],
        "explanation": explanation,
        "cache_hit": False
    }

    query_cache.set(request.query, {
        "query": request.query,
        "recommendations": response_data["recommendations"],
        "explanation": explanation,
        "cache_hit": True
    })

    latency = (time.time() - start_time) * 1000
    app_metrics.record_query(latency, cache_hit=False)

    return RecommendationResponse(
        query=request.query,
        recommendations=recommendations,
        explanation=explanation,
        cache_hit=False
    )


@app.post("/api/ingest")
def ingest_data(request: IngestionRequest):
    if not embedder:
        raise HTTPException(status_code=500, detail="Embedder not initialized.")
    ingest_svc = DataIngestionService(embedder)
    items_dicts = [{"title": i.title, "description": i.description} for i in request.items]
    result = ingest_svc.ingest_items(items_dicts)
    if result["status"] == "error":
        raise HTTPException(status_code=400, detail=result["message"])
    query_cache.clear()
    return result


@app.post("/api/feedback")
def submit_feedback(request: FeedbackRequest):
    try:
        feedback_manager.record_feedback(request.query, request.rating, request.comments)
        return {"status": "success", "message": "Feedback recorded"}
    except ValueError as val_err:
        raise HTTPException(status_code=400, detail=str(val_err))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/metrics")
def get_system_metrics():
    metrics = app_metrics.get_metrics()
    metrics["average_feedback_rating"] = feedback_manager.get_average_rating()
    metrics["total_feedback_received"] = len(feedback_manager.get_all_feedback())
    return metrics