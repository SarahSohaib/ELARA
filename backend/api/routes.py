from fastapi import APIRouter
from backend.services.rag_service import process_query

router = APIRouter()

@router.post("/query")
def query_system(query: str):
    result = process_query(query)
    return {"response": result}