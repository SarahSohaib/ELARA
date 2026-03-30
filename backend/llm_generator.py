import os
import requests
from typing import List, Dict, Any

class LLMGenerator:
    def __init__(self):
        """
        Initializes the LLM Generator using Hugging Face's inference API.
        You should set HF_API_KEY in your .env file or environment variables.
        """
        self.api_key = os.getenv("HF_API_KEY", "")
        # Using a reliable generative model for text (e.g., Mistral or Zephyr)
        self.api_url = "https://api-inference.huggingface.co/models/HuggingFaceH4/zephyr-7b-beta"
        self.headers = {"Authorization": f"Bearer {self.api_key}"}

    def generate_explanation(self, user_query: str, retrieved_items: List[Dict[str, Any]]) -> str:
        """
        Prompts the LLM to generate an explanation for the recommendations.
        """
        if not self.api_key:
            return "Please provide a valid Hugging Face API key to generate an automated explanation."

        context_string = ""
        for i, item in enumerate(retrieved_items):
            context_string += f"Item {i+1}: Title: {item.get('title')}, Description: {item.get('description')}\n"

        prompt = f"""<|system|>
You are a context-aware recommendation engine named ELARA. Below is a user's preference and a list of retrieved items from a semantic search.
Explain why these specific items are great recommendations for the user based exactly on their query. Keep it brief.

<|user|>
User Preference: {user_query}
Retrieved Items Context:
{context_string}
Provide a 2-3 sentence explanation summarizing why these fit the user's preference.
<|assistant|>
"""
        payload = {
            "inputs": prompt,
            "parameters": {
                "max_new_tokens": 150,
                "temperature": 0.5,
                "return_full_text": False
            }
        }

        try:
            response = requests.post(self.api_url, headers=self.headers, json=payload)
            if response.status_code == 200:
                result = response.json()
                explanation = result[0].get("generated_text", "").strip()
                return explanation
            else:
                return f"LLM Generation failed with status {response.status_code}: {response.text}"
        except Exception as e:
            return f"Error contacting LLM API: {str(e)}"
