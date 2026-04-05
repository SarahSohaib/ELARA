from fastapi import APIRouter
from backend.services.rag_service import process_query
from backend.models.query_model import QueryRequest, RecommendationRequest

router = APIRouter()

@router.post("/query")
def query_system(request: QueryRequest):
    result = process_query(request.query)
    return {"response": result}

@router.post("/recommend")
def recommend_system(request: RecommendationRequest):
    combined_query = f"{request.query} {request.mood} {request.genre} {request.era}".strip()
    recommendations = process_query(combined_query)
    return {"recommendations": recommendations}

@router.get("/health")
def health_check():
    return {"status": "ok"}