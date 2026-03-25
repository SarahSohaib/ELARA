// api.js — ELARA Backend Integration
// Connect this to Sarah's FastAPI backend

const BASE_URL = import.meta.env.VITE_API_URL || "http://localhost:8000";

export async function fetchRecommendations({ query, mood, genre, era }) {
  const response = await fetch(`${BASE_URL}/recommend`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({ query, mood, genre, era }),
  });

  if (!response.ok) {
    const error = await response.json().catch(() => ({}));
    throw new Error(error.detail || `Server error: ${response.status}`);
  }

  const data = await response.json();
  return data.recommendations || [];
}

export async function pingBackend() {
  const response = await fetch(`${BASE_URL}/health`);
  return response.ok;
}