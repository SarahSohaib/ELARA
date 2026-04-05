import faiss
import numpy as np
from typing import List, Dict, Any

class VectorDBClient:
    def __init__(self, dimension: int = 384):
        """
        Initializes a FAISS DB index.
        Dimension defaults to 384 because all-MiniLM-L6-v2 produces 384-dimensional embeddings.
        """
        self.dimension = dimension
        # Using IndexFlatL2 for exact nearest neighbors search based on L2 distance
        self.index = faiss.IndexFlatL2(self.dimension)
        # In-memory mock mapping from vector index to item metadata
        self.metadata_store: Dict[int, Dict[str, Any]] = {}
        self.current_id = 0

    def add_items(self, embeddings: np.ndarray, metadata: List[Dict[str, Any]]):
        """
        Adds vectors to the FAISS index and stores corresponding metadata.
        """
        if len(embeddings) != len(metadata):
            raise ValueError("Number of embeddings must match number of metadata items.")

        if embeddings.shape[1] != self.dimension:
            raise ValueError(f"Expected embedding dimension {self.dimension}, got {embeddings.shape[1]}")

        # Ensure embeddings are float32 as FAISS expects
        embeddings = np.array(embeddings, dtype=np.float32)
        
        self.index.add(embeddings)

        # Store metadata mapping
        for item in metadata:
            self.metadata_store[self.current_id] = item
            self.current_id += 1

    def search(self, query_embedding: np.ndarray, top_k: int = 3) -> List[Dict[str, Any]]:
        """
        Searches the DB for the closest vectors to the query embedding.
        Returns a list of dictionaries containing metadata and distance score.
        """
        if query_embedding.shape[1] != self.dimension:
            raise ValueError(f"Expected query dimension {self.dimension}, got {query_embedding.shape[1]}")

        query_embedding = np.array(query_embedding, dtype=np.float32)
        distances, indices = self.index.search(query_embedding, top_k)

        results = []
        for i in range(len(indices[0])):
            idx = int(indices[0][i])
            if idx != -1 and idx in self.metadata_store:
                item_data = self.metadata_store[idx].copy()
                item_data['score'] = float(distances[0][i])
                results.append(item_data)
        
        return results

# Singleton instance to be used across the application
vector_db = VectorDBClient()

# Example mock data initialization for cold-start demo
# Commented out to use real CSV data instead
# mock_data = [
#     {"id": "1", "title": "Sci-Fi Noir", "description": "A dark, gritty detective story set in a dystopian future."},
#     {"id": "2", "title": "Fantasy Epic", "description": "A grand tale of magic, kingdoms, and ancient dragons."},
#     {"id": "3", "title": "Romantic Comedy", "description": "A lighthearted story about two rivals falling in love."}
# ]

# Note: In a real scenario, you'd load the embeddings generated from `embeddings.py` here.
# For simplicity, we initialize mock embeddings if real ones aren't available immediately.
# mock_embeddings = np.random.rand(3, 384).astype('float32')
# vector_db.add_items(mock_embeddings, mock_data)
