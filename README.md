# 🤖 AI Resume Analyzer

An **AI-powered FastAPI** backend that parses, analyzes, and scores resumes (PDF) against job descriptions. It extracts contact information, resume sections, and categorized skills — then returns a structured analysis with a resume score.

---

## ✨ Features

- 📤 **Upload Resume** — accepts PDF files
- 📤 **Upload Job Description** — accepts PDF files or raw text
- 🔍 **Text Extraction** — powered by `pdfplumber`
- 👤 **Contact Parsing** — extracts name, email, and phone number
- 📑 **Section Detection** — identifies Profile, Skills, Experience, Projects, Education
- 🏷️ **Skill Categorization** — maps skills to categories (Programming, Frontend, Backend, Database, DevOps, Cloud, Analytics, AI/ML, Cybersecurity)
- 📊 **Resume Scoring** — scores resume completeness (0–100) based on contact info, sections, and skill count
- 💼 **JD Skill Extraction** — extracts required skills from a job description

---

## 🗂️ Project Structure

```
ai-resume-analyzer/
│
├── backend/
│   ├── main.py                   # FastAPI app & all route definitions
│   │
│   ├── parsers/
│   │   ├── resume_parser.py      # PDF text extraction (pdfplumber)
│   │   ├── section_parser.py     # Resume section detection
│   │   └── info_parser.py        # Name / email / phone extraction
│   │
│   ├── analyzers/
│   │   ├── skill_extractor.py    # Skill detection & categorization
│   │   ├── resume_analyzer.py    # Resume scoring logic
│   │   └── jd_skill_extractor.py # Job description skill extraction
│   │
│   ├── uploads/                  # Uploaded resumes (gitignored)
│   ├── uploads_jd/               # Uploaded JDs (gitignored)
│   ├── reports/                  # Generated reports (gitignored)
│   └── database/                 # Database files (gitignored)
│
├── requirements.txt
├── .gitignore
└── README.md
```

---

## 🚀 Getting Started

### Prerequisites

- Python 3.9+
- pip

### 1. Clone the repository

```bash
git clone https://github.com/your-username/ai-resume-analyzer.git
cd ai-resume-analyzer
```

### 2. Create and activate a virtual environment

```bash
# Windows
python -m venv .venv
.venv\Scripts\activate

# macOS / Linux
python -m venv .venv
source .venv/bin/activate
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

The API will be available at: **http://127.0.0.1:8000**

Interactive docs (Swagger UI): **http://127.0.0.1:8000/docs**

---

## 📡 API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| `GET` | `/` | Health check |
| `POST` | `/upload-resume` | Upload a PDF resume |
| `GET` | `/extract-text` | Extract raw text from uploaded resume |
| `GET` | `/parse-info` | Extract name, email, phone |
| `GET` | `/parse-sections` | Extract resume sections |
| `GET` | `/extract-skills` | Extract categorized skills from resume |
| `GET` | `/resume-summary` | Full summary (contact + sections + skills) |
| `GET` | `/analyze-resume` | Full analysis with resume score |
| `POST` | `/upload-jd` | Upload a PDF job description |
| `GET` | `/extract-jd-text` | Extract raw text from uploaded JD |
| `GET` | `/extract-jd-skills` | Extract skills from uploaded JD |
| `POST` | `/submit-jd` | Submit raw JD text and extract skills |

---

## 🛠️ Tech Stack

| Layer | Technology |
|-------|-----------|
| Framework | [FastAPI](https://fastapi.tiangolo.com/) |
| Server | [Uvicorn](https://www.uvicorn.org/) |
| PDF Parsing | [pdfplumber](https://github.com/jsvine/pdfplumber) |
| Validation | [Pydantic v2](https://docs.pydantic.dev/) |
| Language | Python 3.9+ |

---

## 📦 Skill Categories Detected

| Category | Examples |
|----------|---------|
| Programming Languages | Python, Java, C++, JavaScript, TypeScript |
| Frontend | HTML, CSS, React, Angular, Vue |
| Backend | Django, Flask, FastAPI, Node.js, Spring Boot |
| Database | MySQL, PostgreSQL, MongoDB, SQLite |
| DevOps | Git, Docker, Kubernetes, Jenkins |
| Cloud | AWS, Azure, GCP |
| Analytics | Power BI, Tableau, Excel |
| AI / ML | Machine Learning, TensorFlow, PyTorch |
| Cybersecurity | Ethical Hacking, Network Security |

---

## 🔮 Roadmap

- [ ] Frontend UI (React / Next.js)
- [ ] Resume vs JD match score
- [ ] AI-powered suggestions for resume improvement
- [ ] Multi-resume batch processing
- [ ] Export reports as PDF

---

## 📄 License

This project is licensed under the [MIT License](LICENSE).

---

> **AI Resume Analyzer** — Built with ❤️ using FastAPI & Python
