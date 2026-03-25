# ELARA Frontend 🎯

**Explainable, Context-Aware Recommendation Engine**  
UI/UX built by **Priyanshi** · Role: UI, UX & System Integration Engineer

---

## 🚀 Quick Start

```bash
# Install dependencies
npm install

# Start development server
npm run dev
# → Opens at http://localhost:3000

# Build for production
npm run build
```

---

## 📁 Project Structure

```
elara-frontend/
├── index.html              # HTML entry point
├── vite.config.js          # Vite + proxy config (routes /api → backend)
├── package.json
└── src/
    ├── main.jsx            # React root
    ├── App.jsx             # Main UI component (all screens)
    └── api.js              # Backend API integration layer
```

---

## 🔌 Connecting to Backend (Sarah's API)

When Sarah's FastAPI backend is running:

1. Open `src/App.jsx`
2. Find the comment block `// In production: replace with real API call`
3. Replace the mock delay with:

```js
import { fetchRecommendations } from "./api";

// Inside handleSubmit():
const results = await fetchRecommendations({ query, mood, genre, era });
setRecs(results);
```

The backend should expose:
- `POST /recommend` → `{ recommendations: [...] }`
- `GET /health` → `{ status: "ok" }`

The Vite proxy in `vite.config.js` already routes `/api/*` → `localhost:8000`.

---

## 🎨 UI Features

| Feature | Status |
|---|---|
| Natural language query input | ✅ |
| Mood / Genre / Era filters | ✅ |
| Animated loading + RAG pipeline visualization | ✅ |
| Recommendation cards with match score | ✅ |
| Expandable explanation panel (LLM-generated) | ✅ |
| Responsive layout | ✅ |
| Reset / new search flow | ✅ |

---

## 📋 GitHub Commit Strategy (Priyanshi)

Use this pattern for **all commits**:

```
feat(ui): add recommendation card with score ring
fix(ui): handle empty state when no results returned
style(ui): polish filter dropdowns and spacing
chore: add api.js integration layer for backend connection
docs: update README with setup instructions
```

### Suggested commit sequence to push now:

```bash
git checkout -b feat/priyanshi-ui-core

git add src/App.jsx
git commit -m "feat(ui): build ELARA main interface with query input and filters"

git add src/api.js
git commit -m "feat(ui): add API integration layer for backend connection"

git add index.html vite.config.js package.json
git commit -m "chore: setup Vite React project with proxy config for backend"

git add README.md
git commit -m "docs: add frontend setup guide and commit strategy"

git push origin feat/priyanshi-ui-core
# → Open PR to main
```

---

## 🧠 Course Outcome Alignment

- **CO4**: Advanced LLM + RAG application integration (frontend layer)  
- **CO1**: DevOps practices — Git branching, meaningful commits, CI-ready build

---

## 👤 Role: UI, UX & System Integration Engineer

**Priyanshi** is responsible for:
- ✅ Query input & recommendation display UI
- ✅ Explanation display panel
- ✅ UX flow and usability
- ✅ Frontend–backend integration (`api.js`)
- ✅ Error handling and empty states
- ✅ Demo readiness
Contribution by Priyanshi
