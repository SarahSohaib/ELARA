from typing import List, Dict, Any
import csv
import os
from backend.vector_db import vector_db
from backend.embeddings import Embedder

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

    def load_and_ingest_csv(self) -> Dict[str, Any]:
        csv_path = os.path.join(os.path.dirname(__file__), '..', 'data', 'IMDB-Movie-Dataset(2023-1951).csv')
        if not os.path.exists(csv_path):
            return {"status": "error", "message": f"CSV file not found at {csv_path}"}

        items = []
        try:
            with open(csv_path, 'r', encoding='utf-8') as f:
                reader = csv.DictReader(f)
                for row in reader:
                    item = {
                        "movie_id": row.get("movie_id", ""),
                        "title": row.get("movie_name", ""),
                        "description": f"Year: {row.get('year', '')}. Genre: {row.get('genre', '')}. Overview: {row.get('overview', '')}. Director: {row.get('director', '')}. Cast: {row.get('cast', '')}",
                        "year": row.get("year", ""),
                        "genre": row.get("genre", ""),
                        "director": row.get("director", ""),
                        "cast": row.get("cast", "")
                    }
                    items.append(item)
        except Exception as e:
            return {"status": "error", "message": f"Failed to read CSV: {str(e)}"}

        # Ingest the items
        return self.ingest_items(items)
