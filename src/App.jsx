import { useState, useEffect, useRef } from "react";

const SAMPLE_RECOMMENDATIONS = [
  {
    id: 1,
    title: "Inception",
    type: "Movie",
    year: 2010,
    tags: ["Sci-Fi", "Thriller", "Mind-bending"],
    score: 97,
    explanation:
      "Matched your preference for layered narratives and psychological depth. The dream-within-a-dream structure aligns with your interest in non-linear storytelling and intellectual complexity.",
  },
  {
    id: 2,
    title: "Dark (Series)",
    type: "TV Series",
    year: 2017,
    tags: ["Mystery", "Sci-Fi", "Time Travel"],
    score: 93,
    explanation:
      "Retrieved based on strong semantic overlap with themes of temporal paradox and intricate character webs — consistent with your query's emotional and narrative tone.",
  },
  {
    id: 3,
    title: "Annihilation",
    type: "Movie",
    year: 2018,
    tags: ["Sci-Fi", "Horror", "Existential"],
    score: 88,
    explanation:
      "Surfaced due to high cosine similarity with your described mood: eerie, atmospheric, and philosophically unsettling. Recommended for its unique visual language.",
  },
];

const TypewriterText = ({ text, speed = 18, onDone }) => {
  const [displayed, setDisplayed] = useState("");
  const [done, setDone] = useState(false);
  useEffect(() => {
    setDisplayed("");
    setDone(false);
    let i = 0;
    const interval = setInterval(() => {
      i++;
      setDisplayed(text.slice(0, i));
      if (i >= text.length) {
        clearInterval(interval);
        setDone(true);
        onDone && onDone();
      }
    }, speed);
    return () => clearInterval(interval);
  }, [text]);
  return (
    <span>
      {displayed}
      {!done && <span className="cursor-blink">▌</span>}
    </span>
  );
};

const ScoreRing = ({ score }) => {
  const r = 22;
  const circ = 2 * Math.PI * r;
  const offset = circ - (score / 100) * circ;
  return (
    <svg width="58" height="58" className="score-ring">
      <circle cx="29" cy="29" r={r} stroke="#1e293b" strokeWidth="4" fill="none" />
      <circle
        cx="29" cy="29" r={r}
        stroke="url(#scoreGrad)"
        strokeWidth="4" fill="none"
        strokeDasharray={circ}
        strokeDashoffset={offset}
        strokeLinecap="round"
        transform="rotate(-90 29 29)"
        style={{ transition: "stroke-dashoffset 1.2s cubic-bezier(.4,0,.2,1)" }}
      />
      <defs>
        <linearGradient id="scoreGrad" x1="0%" y1="0%" x2="100%" y2="0%">
          <stop offset="0%" stopColor="#38bdf8" />
          <stop offset="100%" stopColor="#818cf8" />
        </linearGradient>
      </defs>
      <text x="29" y="33" textAnchor="middle" fill="#e2e8f0" fontSize="12" fontWeight="700">
        {score}%
      </text>
    </svg>
  );
};

const RecommendationCard = ({ item, index }) => {
  const [visible, setVisible] = useState(false);
  const [expanded, setExpanded] = useState(false);
  useEffect(() => {
    const t = setTimeout(() => setVisible(true), index * 200);
    return () => clearTimeout(t);
  }, []);

  return (
    <div
      className={`rec-card ${visible ? "rec-card--visible" : ""}`}
      style={{ transitionDelay: `${index * 0.12}s` }}
    >
      <div className="rec-card__header">
        <div>
          <span className="rec-card__type">{item.type}</span>
          <h3 className="rec-card__title">{item.title}</h3>
          <span className="rec-card__year">{item.year}</span>
        </div>
        <ScoreRing score={item.score} />
      </div>
      <div className="rec-card__tags">
        {item.tags.map((t) => (
          <span key={t} className="tag">{t}</span>
        ))}
      </div>
      <div
        className={`rec-card__explanation ${expanded ? "rec-card__explanation--expanded" : ""}`}
        onClick={() => setExpanded(!expanded)}
      >
        <div className="rec-card__explain-label">
          <svg width="13" height="13" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
            <circle cx="12" cy="12" r="10" />
            <line x1="12" y1="8" x2="12" y2="12" />
            <line x1="12" y1="16" x2="12.01" y2="16" />
          </svg>
          Why this was recommended
          <svg
            width="13" height="13" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2"
            style={{ marginLeft: "auto", transform: expanded ? "rotate(180deg)" : "rotate(0deg)", transition: "transform 0.3s" }}
          >
            <polyline points="6 9 12 15 18 9" />
          </svg>
        </div>
        {expanded && <p className="rec-card__explain-text">{item.explanation}</p>}
      </div>
    </div>
  );
};

const ParticlesBg = () => (
  <svg className="particles-bg" xmlns="http://www.w3.org/2000/svg" aria-hidden>
    {[...Array(18)].map((_, i) => (
      <circle
        key={i}
        cx={`${(i * 37 + 10) % 100}%`}
        cy={`${(i * 53 + 5) % 100}%`}
        r={i % 3 === 0 ? 1.5 : 1}
        fill={i % 2 === 0 ? "#38bdf8" : "#818cf8"}
        opacity={0.18 + (i % 4) * 0.06}
        className={`particle particle-${i % 4}`}
      />
    ))}
  </svg>
);

export default function App() {
  const [query, setQuery] = useState("");
  const [mood, setMood] = useState("");
  const [genre, setGenre] = useState("");
  const [era, setEra] = useState("");
  const [recs, setRecs] = useState([]);
  const [phase, setPhase] = useState("idle");
  const [statusMsg, setStatusMsg] = useState("");
  const [charCount, setCharCount] = useState(0);
  const inputRef = useRef(null);

  const moods = ["Thrilling", "Melancholic", "Uplifting", "Eerie", "Thought-provoking", "Cozy"];
  const genres = ["Sci-Fi", "Drama", "Mystery", "Comedy", "Horror", "Documentary"];
  const eras = ["Any", "Classic (pre-1980)", "80s–90s", "2000s", "2010s", "Recent (2020+)"];

  const handleSubmit = async () => {
    if (!query.trim()) return;
    setPhase("thinking");
    setRecs([]);
    const steps = [
      "Embedding your query…",
      "Searching vector database…",
      "Retrieving semantic matches…",
      "Generating explanations via LLM…",
    ];
    for (let i = 0; i < steps.length; i++) {
      setStatusMsg(steps[i]);
      await new Promise((r) => setTimeout(r, 700));
    }
    setRecs(SAMPLE_RECOMMENDATIONS);
    setPhase("results");
  };

  const handleReset = () => {
    setPhase("idle");
    setRecs([]);
    setQuery("");
    setMood("");
    setGenre("");
    setEra("");
    setTimeout(() => inputRef.current?.focus(), 100);
  };

  return (
    <>
      <style>{`
        @import url('https://fonts.googleapis.com/css2?family=Syne:wght@400;600;700;800&family=DM+Sans:wght@300;400;500&display=swap');
        *, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }
        :root {
          --bg: #050d1a; --surface: #0c1a2e; --surface2: #112240;
          --border: rgba(56,189,248,0.12); --accent: #38bdf8; --accent2: #818cf8;
          --text: #e2e8f0; --text-muted: #64748b; --radius: 14px;
        }
        html, body, #root { height: 100%; background: var(--bg); color: var(--text); font-family: 'DM Sans', sans-serif; font-size: 15px; line-height: 1.6; overflow-x: hidden; }
        .app { min-height: 100vh; display: flex; flex-direction: column; align-items: center; padding: 0 1rem 4rem; position: relative; }
        .particles-bg { position: fixed; inset: 0; width: 100%; height: 100%; pointer-events: none; z-index: 0; }
        .particle { animation: float 8s ease-in-out infinite alternate; }
        .particle-0 { animation-duration: 9s; } .particle-1 { animation-duration: 12s; animation-delay: -3s; }
        .particle-2 { animation-duration: 7s; animation-delay: -6s; } .particle-3 { animation-duration: 14s; animation-delay: -1s; }
        @keyframes float { from { transform: translateY(0px); } to { transform: translateY(-18px); } }
        .glow-orb { position: fixed; border-radius: 50%; filter: blur(90px); pointer-events: none; z-index: 0; opacity: 0.12; }
        .glow-orb--1 { width: 500px; height: 500px; background: #38bdf8; top: -150px; left: -100px; }
        .glow-orb--2 { width: 400px; height: 400px; background: #818cf8; bottom: 100px; right: -120px; }
        .header { width: 100%; max-width: 860px; padding: 3.5rem 0 2rem; text-align: center; position: relative; z-index: 1; }
        .header__badge { display: inline-flex; align-items: center; gap: 6px; background: rgba(56,189,248,0.08); border: 1px solid rgba(56,189,248,0.2); border-radius: 100px; padding: 4px 14px; font-size: 11px; font-weight: 600; letter-spacing: 0.12em; text-transform: uppercase; color: var(--accent); margin-bottom: 1.2rem; }
        .header__badge::before { content: ""; display: inline-block; width: 6px; height: 6px; background: var(--accent); border-radius: 50%; animation: pulse 2s infinite; }
        @keyframes pulse { 0%, 100% { opacity: 1; transform: scale(1); } 50% { opacity: 0.4; transform: scale(0.7); } }
        .header__logo { font-family: 'Syne', sans-serif; font-size: clamp(3rem, 8vw, 5.5rem); font-weight: 800; letter-spacing: -0.03em; line-height: 1; background: linear-gradient(135deg, #e2e8f0 30%, #38bdf8 60%, #818cf8 100%); -webkit-background-clip: text; -webkit-text-fill-color: transparent; background-clip: text; margin-bottom: 0.5rem; }
        .header__tagline { font-size: 1rem; color: var(--text-muted); font-weight: 300; }
        .header__tagline strong { color: var(--text); font-weight: 500; }
        .main-card { width: 100%; max-width: 760px; background: var(--surface); border: 1px solid var(--border); border-radius: 20px; padding: 2rem; position: relative; z-index: 1; }
        .query-label { font-family: 'Syne', sans-serif; font-size: 0.78rem; font-weight: 700; letter-spacing: 0.1em; text-transform: uppercase; color: var(--text-muted); margin-bottom: 0.6rem; display: flex; justify-content: space-between; }
        .query-label .char-count { font-family: 'DM Sans', sans-serif; font-weight: 400; font-size: 0.75rem; }
        .query-textarea { width: 100%; background: var(--surface2); border: 1.5px solid var(--border); border-radius: var(--radius); padding: 1rem 1.1rem; color: var(--text); font-family: 'DM Sans', sans-serif; font-size: 0.97rem; resize: none; outline: none; transition: border-color 0.2s; line-height: 1.65; }
        .query-textarea:focus { border-color: var(--accent); box-shadow: 0 0 0 3px rgba(56,189,248,0.08); }
        .query-textarea::placeholder { color: var(--text-muted); }
        .filters { display: grid; grid-template-columns: repeat(3, 1fr); gap: 1rem; margin-top: 1.2rem; }
        @media (max-width: 560px) { .filters { grid-template-columns: 1fr; } }
        .filter-group label { font-family: 'Syne', sans-serif; font-size: 0.7rem; font-weight: 700; letter-spacing: 0.1em; text-transform: uppercase; color: var(--text-muted); display: block; margin-bottom: 0.4rem; }
        .filter-select { width: 100%; background: var(--surface2); border: 1.5px solid var(--border); border-radius: 10px; padding: 0.55rem 0.85rem; color: var(--text); font-family: 'DM Sans', sans-serif; font-size: 0.88rem; outline: none; cursor: pointer; transition: border-color 0.2s; appearance: none; background-image: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='12' height='12' fill='none' stroke='%2364748b' stroke-width='2' viewBox='0 0 24 24'%3E%3Cpolyline points='6 9 12 15 18 9'/%3E%3C/svg%3E"); background-repeat: no-repeat; background-position: right 10px center; padding-right: 30px; }
        .filter-select:focus { border-color: var(--accent2); }
        .submit-row { display: flex; justify-content: flex-end; gap: 0.75rem; margin-top: 1.4rem; }
        .btn { display: inline-flex; align-items: center; gap: 8px; padding: 0.7rem 1.6rem; border-radius: 10px; font-family: 'Syne', sans-serif; font-size: 0.88rem; font-weight: 700; letter-spacing: 0.04em; cursor: pointer; border: none; transition: all 0.2s; }
        .btn--primary { background: linear-gradient(135deg, #38bdf8, #818cf8); color: #050d1a; }
        .btn--primary:hover:not(:disabled) { filter: brightness(1.1); transform: translateY(-1px); box-shadow: 0 6px 24px rgba(56,189,248,0.25); }
        .btn--primary:disabled { opacity: 0.5; cursor: not-allowed; }
        .btn--ghost { background: transparent; color: var(--text-muted); border: 1px solid var(--border); }
        .btn--ghost:hover { color: var(--text); border-color: var(--accent); }
        .thinking-panel { margin-top: 2rem; text-align: center; position: relative; z-index: 1; }
        .thinking-panel__status { color: var(--text-muted); font-size: 0.88rem; min-height: 1.4rem; }
        .thinking-dots { display: flex; justify-content: center; gap: 6px; margin: 1rem 0; }
        .dot { width: 8px; height: 8px; border-radius: 50%; background: var(--accent); animation: dotBounce 1.2s ease-in-out infinite; }
        .dot:nth-child(2) { animation-delay: 0.2s; background: #a78bfa; }
        .dot:nth-child(3) { animation-delay: 0.4s; background: var(--accent2); }
        @keyframes dotBounce { 0%, 80%, 100% { transform: scale(0.6); opacity: 0.5; } 40% { transform: scale(1); opacity: 1; } }
        .results-section { width: 100%; max-width: 760px; position: relative; z-index: 1; margin-top: 2rem; }
        .results-header { display: flex; align-items: center; justify-content: space-between; margin-bottom: 1.2rem; }
        .results-header h2 { font-family: 'Syne', sans-serif; font-size: 1.1rem; font-weight: 700; }
        .results-count { font-size: 0.78rem; color: var(--text-muted); background: var(--surface2); border: 1px solid var(--border); border-radius: 100px; padding: 3px 12px; }
        .rec-card { background: var(--surface); border: 1px solid var(--border); border-radius: var(--radius); padding: 1.3rem 1.4rem; margin-bottom: 1rem; opacity: 0; transform: translateY(18px); transition: opacity 0.4s ease, transform 0.4s ease, border-color 0.2s; }
        .rec-card--visible { opacity: 1; transform: translateY(0); }
        .rec-card:hover { border-color: rgba(56,189,248,0.3); }
        .rec-card__header { display: flex; justify-content: space-between; align-items: flex-start; gap: 1rem; }
        .rec-card__type { font-size: 0.7rem; font-weight: 700; letter-spacing: 0.12em; text-transform: uppercase; color: var(--accent2); }
        .rec-card__title { font-family: 'Syne', sans-serif; font-size: 1.15rem; font-weight: 700; color: var(--text); margin: 2px 0; }
        .rec-card__year { font-size: 0.78rem; color: var(--text-muted); }
        .rec-card__tags { display: flex; flex-wrap: wrap; gap: 6px; margin: 0.75rem 0; }
        .tag { background: rgba(56,189,248,0.07); border: 1px solid rgba(56,189,248,0.15); color: var(--accent); font-size: 0.72rem; font-weight: 600; letter-spacing: 0.05em; padding: 2px 10px; border-radius: 100px; }
        .rec-card__explanation { background: var(--surface2); border: 1px solid var(--border); border-radius: 10px; padding: 0.65rem 0.9rem; cursor: pointer; transition: background 0.2s; }
        .rec-card__explanation:hover { background: rgba(56,189,248,0.05); }
        .rec-card__explain-label { display: flex; align-items: center; gap: 6px; font-size: 0.76rem; font-weight: 600; color: var(--text-muted); }
        .rec-card__explain-text { margin-top: 0.6rem; font-size: 0.85rem; color: var(--text); line-height: 1.65; opacity: 0.9; }
        .pipeline-strip { width: 100%; max-width: 760px; display: flex; align-items: center; justify-content: center; gap: 0; margin: 1.5rem 0 0; position: relative; z-index: 1; }
        .pipeline-step { display: flex; flex-direction: column; align-items: center; gap: 4px; flex: 1; }
        .pipeline-step__icon { width: 36px; height: 36px; border-radius: 50%; background: var(--surface2); border: 1.5px solid var(--border); display: flex; align-items: center; justify-content: center; font-size: 14px; }
        .pipeline-step__icon--active { border-color: var(--accent); background: rgba(56,189,248,0.1); box-shadow: 0 0 12px rgba(56,189,248,0.25); }
        .pipeline-step__label { font-size: 0.62rem; color: var(--text-muted); font-weight: 500; text-align: center; }
        .pipeline-arrow { width: 28px; height: 2px; background: var(--border); flex-shrink: 0; position: relative; top: -10px; }
        .score-ring { flex-shrink: 0; }
        .cursor-blink { animation: blink 0.9s step-end infinite; color: var(--accent); }
        @keyframes blink { 50% { opacity: 0; } }
        .footer { margin-top: 4rem; text-align: center; font-size: 0.75rem; color: var(--text-muted); position: relative; z-index: 1; }
        .footer span { color: var(--accent2); }
      `}</style>

      <div className="app">
        <div className="glow-orb glow-orb--1" />
        <div className="glow-orb glow-orb--2" />
        <ParticlesBg />

        <header className="header">
          <div className="header__badge">RAG · LLM · Semantic Search</div>
          <h1 className="header__logo">ELARA</h1>
          <p className="header__tagline">
            <strong>Explainable</strong> · <strong>Context-Aware</strong> · Recommendation Engine
          </p>
        </header>

        <div className="main-card">
          <div className="query-label">
            <span>Describe what you're looking for</span>
            <span className="char-count">{charCount}/300</span>
          </div>
          <textarea
            ref={inputRef}
            className="query-textarea"
            rows={3}
            maxLength={300}
            placeholder="e.g. A mind-bending sci-fi with layers of mystery, slow burn tension, and a thought-provoking ending…"
            value={query}
            disabled={phase === "thinking"}
            onChange={(e) => { setQuery(e.target.value); setCharCount(e.target.value.length); }}
            onKeyDown={(e) => { if (e.key === "Enter" && (e.ctrlKey || e.metaKey)) handleSubmit(); }}
          />

          <div className="filters">
            <div className="filter-group">
              <label>Mood</label>
              <select className="filter-select" value={mood} onChange={(e) => setMood(e.target.value)} disabled={phase === "thinking"}>
                <option value="">Any mood</option>
                {moods.map((m) => <option key={m}>{m}</option>)}
              </select>
            </div>
            <div className="filter-group">
              <label>Genre</label>
              <select className="filter-select" value={genre} onChange={(e) => setGenre(e.target.value)} disabled={phase === "thinking"}>
                <option value="">Any genre</option>
                {genres.map((g) => <option key={g}>{g}</option>)}
              </select>
            </div>
            <div className="filter-group">
              <label>Era</label>
              <select className="filter-select" value={era} onChange={(e) => setEra(e.target.value)} disabled={phase === "thinking"}>
                {eras.map((e) => <option key={e}>{e}</option>)}
              </select>
            </div>
          </div>

          <div className="submit-row">
            {phase !== "idle" && (
              <button className="btn btn--ghost" onClick={handleReset}>Reset</button>
            )}
            <button
              className="btn btn--primary"
              onClick={handleSubmit}
              disabled={!query.trim() || phase === "thinking"}
            >
              <svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2.5">
                <circle cx="11" cy="11" r="8" /><line x1="21" y1="21" x2="16.65" y2="16.65" />
              </svg>
              {phase === "thinking" ? "Searching…" : "Find for me"}
            </button>
          </div>
        </div>

        {(phase === "thinking" || phase === "results") && (
          <div className="pipeline-strip">
            {[
              { icon: "✍️", label: "Query" },
              { icon: "🔢", label: "Embed" },
              { icon: "🗄️", label: "Vector DB" },
              { icon: "🔗", label: "RAG" },
              { icon: "🤖", label: "LLM" },
              { icon: "💡", label: "Explain" },
            ].map((s, i, arr) => (
              <>
                <div className="pipeline-step" key={s.label}>
                  <div className={`pipeline-step__icon ${phase === "results" ? "pipeline-step__icon--active" : ""}`}>
                    {s.icon}
                  </div>
                  <div className="pipeline-step__label">{s.label}</div>
                </div>
                {i < arr.length - 1 && <div className="pipeline-arrow" key={`a${i}`} />}
              </>
            ))}
          </div>
        )}

        {phase === "thinking" && (
          <div className="thinking-panel">
            <div className="thinking-dots">
              <div className="dot" /><div className="dot" /><div className="dot" />
            </div>
            <p className="thinking-panel__status">
              <TypewriterText key={statusMsg} text={statusMsg} speed={22} />
            </p>
          </div>
        )}

        {phase === "results" && (
          <div className="results-section">
            <div className="results-header">
              <h2>Recommendations for you</h2>
              <span className="results-count">{recs.length} results</span>
            </div>
            {recs.map((item, i) => (
              <RecommendationCard key={item.id} item={item} index={i} />
            ))}
          </div>
        )}

        <footer className="footer">
          ELARA · Built by <span>Priyanshi</span> · LLM + RAG Recommendation Engine
        </footer>
      </div>
    </>
  );
}/ /   m i n o r   u p d a t e  
 / /   m i n o r   u p d a t e  
 