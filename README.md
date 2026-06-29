# 🤖 AI Resume Analyzer

A **FastAPI** backend that parses and analyzes resumes (PDF) against job descriptions. It extracts contact info, resume sections, and skills — then returns a structured analysis with a resume score.

---

## ✨ Features

- 📤 Upload Resume & Job Description (PDF or raw text)
- 👤 Extract name, email, and phone number
- 📑 Detect resume sections — Profile, Skills, Experience, Projects, Education
- 🏷️ Categorize skills — Programming, Frontend, Backend, Database, DevOps, Cloud, AI/ML, etc.
- 📊 Score the resume (0–100) based on completeness
- 💼 Extract required skills from a Job Description

---

## 🗂️ Project Structure

```
ai-resume-analyzer/
│
├── backend/
│   ├── main.py                   # FastAPI app & all routes
│   │
│   ├── parsers/
│   │   ├── resume_parser.py      # PDF text extraction
│   │   ├── section_parser.py     # Resume section detection
│   │   └── info_parser.py        # Name / email / phone extraction
│   │
│   └── analyzers/
│       ├── skill_extractor.py    # Skill detection & categorization
│       ├── resume_analyzer.py    # Resume scoring logic
│       └── jd_skill_extractor.py # JD skill extraction
│
├── requirements.txt
├── .gitignore
└── README.md
```

---

## 🚀 Getting Started

### Prerequisites
- Python 3.9+

### 1. Clone the repository

```bash
git clone https://github.com/prajwaljm123/ai-resume-analyzer.git
cd ai-resume-analyzer
```

### 2. Create and activate a virtual environment

```bash
python -m venv .venv
.venv\Scripts\activate      # Windows
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Run the server

```bash
cd backend
uvicorn main:app --reload
```

- API: **http://127.0.0.1:8000**
- Swagger Docs: **http://127.0.0.1:8000/docs**

---

## 📡 API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| `GET` | `/` | Health check |
| `POST` | `/upload-resume` | Upload a PDF resume |
| `GET` | `/extract-text` | Extract raw text from resume |
| `GET` | `/parse-info` | Extract name, email, phone |
| `GET` | `/parse-sections` | Extract resume sections |
| `GET` | `/extract-skills` | Extract categorized skills |
| `GET` | `/resume-summary` | Full summary (contact + sections + skills) |
| `GET` | `/analyze-resume` | Full analysis with resume score |
| `POST` | `/upload-jd` | Upload a PDF job description |
| `GET` | `/extract-jd-skills` | Extract skills from JD |
| `POST` | `/submit-jd` | Submit raw JD text & extract skills |

---

## 🛠️ Tech Stack

| | Technology |
|---|---|
| Framework | FastAPI |
| Server | Uvicorn |
| PDF Parsing | pdfplumber |
| Language | Python 3.9+ |
