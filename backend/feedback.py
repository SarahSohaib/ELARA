from typing import List, Dict, Any
import datetime

class FeedbackManager:
    def __init__(self):
        """
        Manages explicit user feedback on recommendations.
        Useful for evaluating RAG quality and potential RLHF down the line.
        """
        # In a real app, this would be a database table.
        self.feedback_store: List[Dict[str, Any]] = []

    def record_feedback(self, query: str, rating: int, comments: str = "") -> None:
        """
        Record a user's satisfaction with a recommendation block.
        Rating: 1 (poor) to 5 (excellent)
        """
        if not (1 <= rating <= 5):
            raise ValueError("Rating must be between 1 and 5")

        feedback_entry = {
            "timestamp": datetime.datetime.now().isoformat(),
            "query": query,
            "rating": rating,
            "comments": comments
        }
        self.feedback_store.append(feedback_entry)

    def get_all_feedback(self) -> List[Dict[str, Any]]:
        return self.feedback_store

    def get_average_rating(self) -> float:
        """
        Calculate the average rating across all queries.
        """
        if not self.feedback_store:
            return 0.0
        total = sum(entry["rating"] for entry in self.feedback_store)
        return round(total / len(self.feedback_store), 2)

# Global feedback instance
feedback_manager = FeedbackManager()
