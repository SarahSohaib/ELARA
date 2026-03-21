from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Optional

# Import the new modules for the recommendation subsystem
from models import RecommendationRequest, RecommendationResponse, RecommendedItem
from embeddings import Embedder
from vector_db import vector_db
from llm_generator import LLMGenerator

# Initialize subsystems
try:
    embedder = Embedder()
except Exception as e:
    print(f"Warning: Could not initialize embedder: {e}")
    embedder = None
llm_gen = LLMGenerator()

app = FastAPI(title="ELARA Backend")

class ChatRequest(BaseModel):
    message: str

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
    """
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

    # Step 3: LLM generation for explainability (grounded in the retrieved data)
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

    return RecommendationResponse(
        query=request.query,
        recommendations=recommendations,
        explanation=explanation
    )
