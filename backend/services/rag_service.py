from backend.vector_db import vector_db
from backend.embeddings import Embedder

embedder = Embedder()

def process_query(query: str, top_k: int = 3) -> list:
    """
    Processes a user query by generating embeddings and searching the vector database.
    Returns a list of recommendation dictionaries.
    """
    try:
        # Generate embedding for the query
        query_embedding = embedder.generate_embeddings([query])
        
        # Search the vector database
        results = vector_db.search(query_embedding, top_k=top_k)
        
        if not results:
            # Fallback: return a mock recommendation if no matches found
            mock_item = {
                "movie_id": "fallback1",
                "title": "Sample Movie",
                "description": "Year: 2023. Genre: Drama. Overview: A sample movie for testing the system. Director: Sample Director. Cast: Sample Cast",
                "year": "2023",
                "genre": "Drama",
                "director": "Sample Director",
                "cast": "Sample Cast"
            }
            results = [mock_item]
        
        recommendations = []
        for i, item in enumerate(results):
            title = item.get('title', 'Unknown Title')
            year = item.get('year', 'Unknown Year')
            genre = item.get('genre', 'Unknown Genre')
            tags = genre.split(', ') if genre else []
            overview = item.get('description', '').split('. Overview: ')[-1] if 'Overview:' in item.get('description', '') else item.get('description', '')
            score = 95 - i * 5  # Decreasing scores for top results
            explanation = f"Recommended based on your query. Overview: {overview[:100]}..."
            
            rec = {
                "id": item.get('movie_id', ''),
                "title": title,
                "type": "Movie",
                "year": int(year) if year.isdigit() else 0,
                "tags": tags,
                "score": score,
                "explanation": explanation
            }
            recommendations.append(rec)
        
        return recommendations
    except Exception as e:
        print(f"Error in process_query: {str(e)}")
        return []
