from typing import Dict, Any
import time

class MetricsTracker:
    def __init__(self):
        """
        Tracks basic operational metrics for the recommendation engine
        like query count, cache hits, and average latency.
        """
        self.total_queries = 0
        self.cache_hits = 0
        self.total_latency_ms = 0.0

    def record_query(self, latency_ms: float, cache_hit: bool = False) -> None:
        """
        Record a single recommendation request's performance.
        """
        self.total_queries += 1
        self.total_latency_ms += latency_ms
        if cache_hit:
            self.cache_hits += 1

    def get_metrics(self) -> Dict[str, Any]:
        """
        Returns a summary of current system performance.
        """
        avg_latency = 0.0
        if self.total_queries > 0:
            avg_latency = round(self.total_latency_ms / self.total_queries, 2)

        cache_hit_rate = 0.0
        if self.total_queries > 0:
            cache_hit_rate = round((self.cache_hits / self.total_queries) * 100, 2)

        return {
            "total_queries_served": self.total_queries,
            "cache_hits": self.cache_hits,
            "cache_hit_rate_percent": cache_hit_rate,
            "average_latency_ms": avg_latency
        }

# Global instances
app_metrics = MetricsTracker()
