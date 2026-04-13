# ELARA 🎯

**ELARA – Explainable Language-Driven AI-Based Recommendation Assistant**

Built using **React + FastAPI + RAG (Retrieval-Augmented Generation)**
UI/UX by **Priyanshi** · Backend & Architecture by **Sarah** · Data by **Adyasha**

---

## 🚀 Quick Start (Frontend)

```bash
# Navigate to frontend
cd ui

# Install dependencies
npm install

# Start development server
npm run dev
# → Opens at http://localhost:3000

# Build for production
npm run build
```

---S

## 📁 Project Structure

```
ELARA/
├── backend/              # FastAPI backend (RAG + APIs)
├── ui/                  # React frontend
│   ├── index.html
│   ├── vite.config.js   # Proxy config (/api → backend)
│   ├── package.json
│   └── src/
│       ├── main.jsx
│       ├── App.jsx
│       └── api.js
├── data/
│   └── data.csv         # Dataset used for recommendations
```

---

## 🔌 System Architecture

```
User Input → React UI → API Call → FastAPI Backend → Data / RAG → Response → UI Render
```

---

## 🔁 Frontend–Backend Integration

### Development Mode

Vite proxy automatically routes:

```
/api → http://localhost:8000
```

---

### Production Mode

Update API calls in `App.jsx`:

```js
fetch("https://your-backend.onrender.com/api/recommend")
```

---

## 📡 API Contract

### POST `/api/recommend`

Request:

```json
{
  "query": "string"
}
```

Response:

```json
{
  "recommendations": [
    {
      "id": 1,
      "title": "string",
      "type": "Movie",
      "year": 2020,
      "tags": ["string"],
      "score": 90,
      "explanation": "string"
    }
  ]
}
```

---

### GET `/api/health`

```json
{ "status": "ok" }
```

---

## 🎨 UI Features

| Feature                         | Status |
| ------------------------------- | ------ |
| Natural language query input    | ✅      |
| Mood / Genre / Era filters      | ✅      |
| RAG pipeline visualization      | ✅      |
| Recommendation cards with score | ✅      |
| Expandable explanation panel    | ✅      |
| Responsive layout               | ✅      |
| Reset / new search flow         | ✅      |

---

## 🧠 Core Capabilities

* Context-aware recommendations using natural language queries
* Explainable outputs powered by LLM logic
* Data-driven filtering via dataset (`data.csv`)
* Modular full-stack architecture
* Designed for extensibility into full RAG pipeline

---

## 📊 Data Layer

* Dataset stored in: `data/data.csv`
* Used for:

  * Filtering and matching user queries
  * Generating recommendations
* Prepared and cleaned before backend ingestion

---

## 📋 Git Commit Strategy

```
feat(ui): add recommendation card with score ring
fix(ui): handle empty state when no results returned
style(ui): polish filters and layout
chore: add API integration layer
docs: update README
```

---

## 👤 Team Roles

### 🔹 Sarah — Project Lead, Backend Engineer & Repository Owner

* Defines overall system architecture
* Implements RAG pipeline and LLM integration
* Designs and develops backend APIs (FastAPI)
* Handles recommendation and explanation logic
* Implements embeddings, vector database, and retrieval logic
* Performs retrieval tuning and evaluation
* Manages GitHub repository (branching, structure, commits)
* Leads system integration and ensures frontend-backend connectivity
* Prepares architecture explanation and viva

👉 Owns: **Backend + RAG + Retrieval + Logic + Integration**

---

### 🔹 Adyasha — Data Engineer

* Dataset sourcing and validation
* Data cleaning and preprocessing
* Data formatting and structuring for ingestion
* Preparing datasets for embedding and backend usage
* Maintaining dataset consistency and documentation

👉 Owns: **Data Preparation Layer**

---

### 🔹 Priyanshi — UI, UX & System Integration Engineer

* Designs and implements user interface
* Builds query input and recommendation display
* Develops explanation UI
* Handles frontend–backend API integration
* Manages UX flow and usability
* Implements error handling and empty states
* Prepares demo-ready interface

👉 Owns: **User Experience + Frontend + Integration Layer**

---

## 🧠 Course Outcome Alignment

* **CO4**: Implementation of advanced LLM + RAG system + VectorDB
* **CO1**: Application of DevOps practices (Git, modular architecture)

---

## 🚀 Deployment Overview

| Component | Platform              |
| --------- | --------------------- |
| Frontend  | GitHub Pages / Vercel |
| Backend   | Render / Railway      |
| Data      | CSV / Vector DB       |

---

## ⚠️ Important Notes

* GitHub Pages hosts only the frontend (static files)
* Backend must be deployed separately
* Replace all `localhost` API calls before deployment

---

## 🎯 Project Goal

ELARA is designed to move beyond traditional recommendation systems by providing:

* Explainable recommendations (not black-box output)
* Context-aware reasoning based on user input
* Integration of retrieval + generation (RAG concept)
* A clean, intuitive user interface

---

## 👥 Contribution Summary

| Member    | Contribution                             |
| --------- | ---------------------------------------- |
| Sarah     | Backend, RAG pipeline, API, architecture |
| Adyasha   | Data preparation, dataset pipeline       |
| Priyanshi | UI, UX, frontend integration             |

---

## 🔥 Final Note

ELARA demonstrates a complete **AI-powered full-stack system**, combining:

* React frontend
* FastAPI backend
* Data pipeline
* Explainable recommendation logic

---
