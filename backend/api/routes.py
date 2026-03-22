from fastapi import APIRouter
from backend.services.rag_service import process_query
from backend.models.query_model import QueryRequest

router = APIRouter()

@router.post("/query")
def query_system(request: QueryRequest):
    result = process_query(request.query)
    return {"response": result}