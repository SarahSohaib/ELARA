import time
from typing import Dict, Any, Optional

class SemanticCache:
    def __init__(self, expiration_seconds: int = 3600):
        """
        A simple in-memory cache to store responses for frequent queries.
        Reduces latency and LLM API costs.
        """
        self.cache: Dict[str, Dict[str, Any]] = {}
        self.expiration_seconds = expiration_seconds

    def get(self, query: str) -> Optional[Dict[str, Any]]:
        """
        Retrieve a cached response if it exists and is not expired.
        """
        query_lower = query.strip().lower()
        if query_lower in self.cache:
            entry = self.cache[query_lower]
            if time.time() - entry["timestamp"] < self.expiration_seconds:
                return entry["data"]
            else:
                # Expired
                del self.cache[query_lower]
        return None

    def set(self, query: str, data: Dict[str, Any]) -> None:
        """
        Store a generated recommendation response in the cache.
        """
        self.cache[query.strip().lower()] = {
            "timestamp": time.time(),
            "data": data
        }

    def clear(self) -> None:
        """
        Clears the entire cache (useful after data ingestions).
        """
        self.cache.clear()

# Global cache instance
query_cache = SemanticCache()
