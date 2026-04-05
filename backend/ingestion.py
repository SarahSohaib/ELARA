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
            combined_text = f"Title: {title}. Description: {desc}"
            texts_to_embed.append(combined_text)

        try:
            new_embeddings = self.embedder.generate_embeddings(texts_to_embed)
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

    def _standardize_row(self, row: Dict[str, str], source: str) -> Dict[str, Any]:
        title = row.get("movie_title") or row.get("movie_name") or row.get("title") or "Unknown Title"
        movie_id = row.get("movie_id") or row.get("id") or title
        year = row.get("year") or row.get("release_year") or ""
        genre = row.get("genre") or ""
        director = row.get("director") or ""
        cast = row.get("cast") or row.get("cast_names") or ""
        language = row.get("language") or ""
        duration = row.get("duration_min") or ""
        overview = row.get("overview") or row.get("user_review") or ""
        sentiment = row.get("sentiment") or ""
        rating = row.get("rating") or ""

        description_parts = [
            f"Year: {year}" if year else None,
            f"Genre: {genre}" if genre else None,
            f"Language: {language}" if language else None,
            f"Duration: {duration} minutes" if duration else None,
            f"Director: {director}" if director else None,
            f"Overview: {overview}" if overview else None,
            f"Sentiment: {sentiment}" if sentiment else None,
            f"Rating: {rating}" if rating else None,
            f"Source: {source}"
        ]
        description = ". ".join([part for part in description_parts if part])

        return {
            "movie_id": movie_id,
            "title": title,
            "description": description,
            "year": year,
            "genre": genre,
            "director": director,
            "cast": cast,
            "source": source
        }

    def _load_csv_file(self, csv_path: str, source: str) -> List[Dict[str, Any]]:
        items = []
        with open(csv_path, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                items.append(self._standardize_row(row, source))
        return items

    def load_and_ingest_csv(self) -> Dict[str, Any]:
        csv_files = [
            'IMDB-Movie-Dataset(2023-1951).csv',
            'hollywood movie dataset.csv'
        ]
        base_dir = os.path.join(os.path.dirname(__file__), '..', 'data')

        all_items = []
        missing_files = []
        loaded_files = []

        for csv_file in csv_files:
            csv_path = os.path.join(base_dir, csv_file)
            if not os.path.exists(csv_path):
                missing_files.append(csv_file)
                continue

            try:
                items = self._load_csv_file(csv_path, csv_file)
                all_items.extend(items)
                loaded_files.append(csv_file)
            except Exception as e:
                return {"status": "error", "message": f"Failed to read {csv_file}: {str(e)}"}

        if not all_items:
            if missing_files:
                return {"status": "error", "message": f"No dataset files found. Missing: {', '.join(missing_files)}"}
            return {"status": "error", "message": "No items were loaded from the dataset files."}

        ingestion_result = self.ingest_items(all_items)
        if missing_files:
            ingestion_result["warning"] = f"Some datasets were missing and were not loaded: {', '.join(missing_files)}"
        ingestion_result["loaded_files"] = loaded_files
        ingestion_result["total_items"] = len(all_items)
        return ingestion_result
