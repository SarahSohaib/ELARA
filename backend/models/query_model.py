from pydantic import BaseModel

class QueryRequest(BaseModel):
    query: str

class RecommendationRequest(BaseModel):
    query: str
    mood: str = ""
    genre: str = ""
    era: str = ""