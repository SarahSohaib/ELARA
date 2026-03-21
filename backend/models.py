from pydantic import BaseModel
from typing import List, Optional

class RecommendationRequest(BaseModel):
    query: str
    top_k: Optional[int] = 3

class RecommendedItem(BaseModel):
    id: str
    title: str
    description: str
    score: float

class RecommendationResponse(BaseModel):
    query: str
    recommendations: List[RecommendedItem]
    explanation: str
