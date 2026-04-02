import faiss
import numpy as np
from typing import List, Dict, Any

class VectorDBClient:
    def __init__(self, dimension: int = 384):
        self.dimension = dimension
        self.index = faiss.IndexFlatL2(self.dimension)
        self.metadata_store: Dict[int, Dict[str, Any]] = {}
        self.current_id = 0

    def add_items(self, embeddings: np.ndarray, metadata: List[Dict[str, Any]]):
        if len(embeddings) != len(metadata):
            raise ValueError("Number of embeddings must match number of metadata items.")
        if embeddings.shape[1] != self.dimension:
            raise ValueError(f"Expected embedding dimension {self.dimension}, got {embeddings.shape[1]}")
        embeddings = np.array(embeddings, dtype=np.float32)
        self.index.add(embeddings)
        for item in metadata:
            self.metadata_store[self.current_id] = item
            self.current_id += 1

    def search(self, query_embedding: np.ndarray, top_k: int = 3) -> List[Dict[str, Any]]:
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


vector_db = VectorDBClient()

mock_data = [
    {"id": "1", "title": "Interstellar", "description": "A sci-fi epic about astronauts travelling through a wormhole near Saturn to find a new home for humanity. Themes of love, time, and survival."},
    {"id": "2", "title": "Inception", "description": "A mind-bending thriller where a thief enters people's dreams to plant an idea. Complex narrative layers and stunning visuals."},
    {"id": "3", "title": "The Matrix", "description": "A hacker discovers reality is a simulation controlled by machines. Iconic action sequences and philosophical themes about reality."},
    {"id": "4", "title": "The Notebook", "description": "A romantic drama about a couple whose love is tested across decades. Emotional and heartfelt storytelling."},
    {"id": "5", "title": "Dune", "description": "An epic science fiction saga about a desert planet, political intrigue, and a chosen one destined to lead a revolution."},
    {"id": "6", "title": "Pride and Prejudice", "description": "A classic romance about Elizabeth Bennet and Mr Darcy navigating social class and personal pride in 19th century England."},
]

try:
    from backend.embeddings import Embedder
    _embedder = Embedder()
    _texts = [f"{item['title']}. {item['description']}" for item in mock_data]
    _embeddings = _embedder.generate_embeddings(_texts)
    vector_db.add_items(_embeddings.astype('float32'), mock_data)
    print(f"Vector DB initialized with {len(mock_data)} real semantic embeddings.")
except Exception as e:
    print(f"Warning: Could not generate real embeddings for mock data, using random: {e}")
    mock_embeddings = np.random.rand(len(mock_data), 384).astype('float32')
    vector_db.add_items(mock_embeddings, mock_data)