// api.js — ELARA Backend Integration
// Connect this to Sarah's FastAPI backend

// For local development, requests go through Vite proxy (/api -> http://localhost:8000)
// For production on GitHub Pages, the backend must be accessible via CORS at the API URL
const BASE_URL = import.meta.env.VITE_API_URL || (import.meta.env.PROD ? 'http://localhost:8000' : "");

export async function fetchRecommendations({ query, mood, genre, era }) {
  console.log('Fetching recommendations from:', `${BASE_URL}/api/recommend`, 'with data:', { query, mood, genre, era });
  const response = await fetch(`${BASE_URL}/api/recommend`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({ query, mood, genre, era }),
  });

  if (!response.ok) {
    const error = await response.json().catch(() => ({}));
    console.error('Fetch failed with status:', response.status, 'error:', error);
    throw new Error(error.detail || `Server error: ${response.status}`);
  }

  const data = await response.json();
  console.log('Received data:', data);
  return data.recommendations || [];
}

export async function pingBackend() {
  const response = await fetch(`${BASE_URL}/api/health`);
  return response.ok;
}