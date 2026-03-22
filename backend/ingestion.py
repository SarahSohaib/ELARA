from typing import List, Dict, Any
from vector_db import vector_db
from embeddings import Embedder

class DataIngestionService:
    def __init__(self, embedder: Embedder):
        self.embedder = embedder

    def ingest_items(self, items: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Takes a list of new items (e.g., movies, books),
        generates embeddings for their descriptions, 
        and adds them to the live vector database.
        """
        if not items:
            return {"status": "error", "message": "No items provided"}

        # Extract descriptions for embedding
        texts_to_embed = []
        for item in items:
            title = item.get("title", "Unknown Title")
            desc = item.get("description", "")
            # Combining title and description gives better semantic context
            combined_text = f"Title: {title}. Description: {desc}"
            texts_to_embed.append(combined_text)

        try:
            # Generate embeddings for the new items
            new_embeddings = self.embedder.generate_embeddings(texts_to_embed)
            
            # Add to FAISS Vector DB
            vector_db.add_items(new_embeddings, items)
            
            return {
                "status": "success", 
                "message": f"Successfully ingested {len(items)} new items into the Vector DB."
            }
        except Exception as e:
            return {
                "status": "error", 
                "message": f"Ingestion failed: {str(e)}"
            }
