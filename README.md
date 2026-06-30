# ⚡ AI Resume Analyzer

A **full-stack ATS resume analyzer** built with **FastAPI + React**. Upload your PDF resume, paste a job description, and instantly get an ATS match score with matched and missing skills highlighted.

---

## ✨ Features

- 📤 **Resume Upload** — drag-and-drop PDF upload with validation
- 📋 **JD Paste** — paste any job description (LinkedIn, Naukri, Indeed, etc.)
- 📊 **ATS Match Score** — custom scoring algorithm (0–100) with animated score ring
- ✅ **Matched Skills** — skills found in both resume and JD
- ❌ **Missing Skills** — skills required by JD but absent from resume
- 🏷️ **Skill Categorization** — Programming, Frontend, Backend, Database, DevOps, Cloud, AI/ML
- 👤 **Contact Extraction** — name, email, phone from resume
- 🌙 **Dark Theme UI** — premium dark design with responsive layout

---

## 🗂️ Project Structure

```
ai-resume-analyzer/
│
├── backend/
│   ├── main.py                    # FastAPI app, all routes, CORS
│   │
│   ├── parsers/
│   │   ├── resume_parser.py       # PDF text extraction (pdfplumber)
│   │   ├── jd_parser.py           # JD PDF text extraction
│   │   ├── section_parser.py      # Resume section detection
│   │   └── info_parser.py         # Name / email / phone extraction
│   │
│   └── analyzers/
│       ├── skill_extractor.py     # Skill detection & categorization
│       ├── resume_analyzer.py     # Resume completeness scoring
│       ├── jd_skill_extractor.py  # JD skill extraction
│       └── jd_matcher.py          # Resume vs JD skill matching + ATS score
│
├── frontend/
│   ├── src/
│   │   ├── App.jsx                # Root component, state management
│   │   ├── App.css                # Full design system (dark theme)
│   │   ├── api/
│   │   │   └── api.js             # Axios client (proxied via Vite)
│   │   └── components/
│   │       ├── ResumeUpload.jsx   # Drag-drop upload → POST /upload-resume
│   │       ├── JDInput.jsx        # JD textarea → POST /match-jd
│   │       └── ResultsPanel.jsx   # ATS score ring + skill pills
│   ├── vite.config.js             # Vite dev proxy → FastAPI backend
│   └── package.json
│
├── requirements.txt
├── .gitignore
└── README.md
```

---

## 🚀 Getting Started

### Prerequisites
- Python 3.9+
- Node.js 18+

---

### Backend Setup

```bash
# 1. Clone the repo
git clone https://github.com/prajwaljm123/ai-resume-analyzer.git
cd ai-resume-analyzer

# 2. Create & activate virtual environment
python -m venv .venv
.venv\Scripts\activate        # Windows
# source .venv/bin/activate   # macOS / Linux

# 3. Install Python dependencies
pip install -r requirements.txt

# 4. Start the backend
cd backend
uvicorn main:app --reload
```

- API: **http://127.0.0.1:8000**
- Swagger Docs: **http://127.0.0.1:8000/docs**

---

### Frontend Setup

```bash
# In a new terminal, from the project root:
cd frontend

# Install Node dependencies
npm install

# Start the dev server (proxies API calls to backend automatically)
npm run dev
```

- App: **http://localhost:5173**

> The Vite dev server proxies all `/api/*` requests to `http://127.0.0.1:8000` — no CORS issues in development.

---

## 📡 API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| `GET` | `/` | Health check |
| `POST` | `/upload-resume` | Upload a PDF resume |
| `GET` | `/extract-text` | Extract raw text from resume |
| `GET` | `/parse-info` | Extract name, email, phone |
| `GET` | `/parse-sections` | Detect resume sections |
| `GET` | `/extract-skills` | Extract categorized skills |
| `GET` | `/resume-summary` | Full summary (contact + sections + skills) |
| `GET` | `/analyze-resume` | Full analysis with resume score |
| `POST` | `/upload-jd` | Upload a PDF job description |
| `GET` | `/extract-jd-skills` | Extract skills from JD |
| `POST` | `/match-jd` | Match resume vs JD text → ATS score |
| `POST` | `/match-jd-pdf` | Match resume vs JD PDF → ATS score |

---

## 🛠️ Tech Stack

| Layer | Technology |
|---|---|
| Backend Framework | FastAPI |
| Server | Uvicorn |
| PDF Parsing | pdfplumber |
| Language | Python 3.9+ |
| Frontend Framework | React 19 + Vite |
| HTTP Client | Axios |
| Styling | Vanilla CSS (dark design system) |
| Dev Proxy | Vite server proxy |

---

## 🔄 How It Works

```
1. User uploads PDF resume  →  POST /upload-resume  →  saved to backend/uploads/
2. User pastes job description text
3. POST /match-jd  →  extracts JD skills  →  compares with resume skills
4. ATS Score calculated:
      - Skill match %          → up to 60 pts
      - Category coverage      → up to 20 pts
      - Core skill presence    → up to 10 pts
      - Missing skill penalty  → up to -10 pts
5. Frontend renders score ring + matched/missing skill pills
```
