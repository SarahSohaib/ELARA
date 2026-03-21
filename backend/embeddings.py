try:
    from sentence_transformers import SentenceTransformer
except ImportError:
    # Fallback or pass for environments where sentence_transformers is not installed immediately
    pass
import numpy as np
from typing import List

class Embedder:
    def __init__(self, model_name: str = "all-MiniLM-L6-v2"):
        """
        Initializes the sentence transformer model.
        all-MiniLM-L6-v2 is a small, fast model ideal for initial development.
        """
        try:
            self.model = SentenceTransformer(model_name)
        except NameError:
            self.model = None
            print("Warning: SentenceTransformer not available. Install sentence-transformers.")

    def generate_embeddings(self, texts: List[str]) -> np.ndarray:
        """
        Converts a list of texts into vector embeddings.
        Returns a numpy array of embeddings.
        """
        if not self.model:
            return np.zeros((len(texts), 384)) # Mock response if model unavailable
        
        # model.encode returns a numpy array representing the embeddings
        embeddings = self.model.encode(texts, convert_to_numpy=True)
        return embeddings

    def embed_query(self, query: str) -> np.ndarray:
        """
        Embeds a single user query.
        """
        if not self.model:
            return np.zeros((1, 384))
        
        return self.model.encode([query], convert_to_numpy=True)
