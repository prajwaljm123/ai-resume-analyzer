from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from parsers.resume_parser import extract_text_from_pdf
from parsers.jd_parser import extract_text_from_jd_pdf

from parsers.section_parser import parse_sections

from analyzers.skill_extractor import (
    extract_skills,
    flatten_skills
)

from parsers.info_parser import (
    extract_name,
    extract_email,
    extract_phone
)
from analyzers.resume_analyzer import analyze_resume
from analyzers.jd_skill_extractor import extract_jd_skills
from analyzers.jd_matcher import match_jd
from services.ai_service import generate_resume_feedback

import os
from dotenv import load_dotenv

# Load .env from the backend directory
load_dotenv()

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173",
        "http://localhost:3000",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class JDRequest(BaseModel):
    jd_text: str

class FeedbackRequest(BaseModel):
    resume_text: str
    jd_text: str
    ats_score: int
    matched_skills: list[str] = []
    missing_skills: list[str] = []

UPLOAD_FOLDER = "uploads"

os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# Job Description Upload Folder

JD_FOLDER = "uploads_jd"

os.makedirs(JD_FOLDER, exist_ok=True)

@app.get("/")
def home():
    return {
        "message": "Resume Analyzer API Running"
    }


@app.post("/upload-resume")
async def upload_resume(file: UploadFile = File(...)):

    file_path = os.path.join(UPLOAD_FOLDER, file.filename)

    with open(file_path, "wb") as buffer:
        buffer.write(await file.read())

    return {
        "message": "Resume uploaded successfully",
        "filename": file.filename
    }
    
@app.get("/extract-text")
def extract_text():

    files = os.listdir("uploads")

    if not files:
        return {"error": "No PDF uploaded"}

    pdf_path = os.path.join("uploads", files[0])

    text = extract_text_from_pdf(pdf_path)

    return {
        "filename": files[0],
        "text": text
    }
    
@app.get("/parse-info")
def parse_info():

    files = os.listdir("uploads")

    if not files:
        return {"error": "No PDF uploaded"}

    pdf_path = os.path.join("uploads", files[0])

    text = extract_text_from_pdf(pdf_path)

    return {
        "name": extract_name(text),
        "email": extract_email(text),
        "phone": extract_phone(text)
    }
    

@app.get("/parse-sections")
def parse_resume_sections():

    files = os.listdir("uploads")

    if not files:
        return {
            "error": "No PDF uploaded"
        }

    pdf_path = os.path.join("uploads", files[0])

    text = extract_text_from_pdf(pdf_path)

    sections = parse_sections(text)

    return sections

@app.get("/extract-skills")
def get_skills():

    files = os.listdir("uploads")

    if not files:
        return {"error": "No PDF uploaded"}

    pdf_path = os.path.join("uploads", files[0])

    text = extract_text_from_pdf(pdf_path)

    skills = extract_skills(text)

    return {
        "skills": skills
    }
    
@app.get("/resume-summary")
def get_resume_summary():

    files = os.listdir(UPLOAD_FOLDER)

    if not files:
        return {
            "success": False,
            "message": "No resume uploaded"
        }

    pdf_path = os.path.join(UPLOAD_FOLDER, files[0])

    text = extract_text_from_pdf(pdf_path)

    contact = {
        "name": extract_name(text),
        "email": extract_email(text),
        "phone": extract_phone(text)
    }

    sections = parse_sections(text)

    categorized_skills = extract_skills(text)

    all_skills = flatten_skills(categorized_skills)

    return {
        "success": True,
        "resume_name": files[0],

        "contact": contact,

        "sections": sections,

        "skills": {
            "categorized": categorized_skills,
            "all": all_skills,
            "total_skills_found": len(all_skills)
        }
    }
    
@app.get("/analyze-resume")
def analyze_uploaded_resume():

    files = os.listdir(UPLOAD_FOLDER)

    if not files:
        return {
            "success": False,
            "message": "No resume uploaded"
        }

    pdf_path = os.path.join(UPLOAD_FOLDER, files[0])

    text = extract_text_from_pdf(pdf_path)

    contact = {
        "name": extract_name(text),
        "email": extract_email(text),
        "phone": extract_phone(text)
    }

    sections = parse_sections(text)

    categorized_skills = extract_skills(text)

    all_skills = []

    for skill_list in categorized_skills.values():
        all_skills.extend(skill_list)

    skills = {
        "categorized": categorized_skills,
        "all": sorted(set(all_skills))
    }

    analysis = analyze_resume(
        contact,
        sections,
        skills
    )

    return analysis


# Job description analysis endpoint

@app.post("/upload-jd")
async def upload_jd(file: UploadFile = File(...)):

    file_path = os.path.join(JD_FOLDER, file.filename)

    with open(file_path, "wb") as buffer:
        buffer.write(await file.read())

    return {
        "message": "JD uploaded successfully",
        "filename": file.filename
    }
    
@app.get("/extract-jd-text")
def extract_jd_text():

    files = os.listdir(JD_FOLDER)

    if not files:
        return {
            "error": "No JD uploaded"
        }

    pdf_path = os.path.join(JD_FOLDER, files[0])

    text = extract_text_from_pdf(pdf_path)

    return {
        "filename": files[0],
        "text": text
    }
    
@app.get("/extract-jd-skills")
def get_jd_skills():

    files = os.listdir(JD_FOLDER)

    if not files:
        return {
            "error": "No JD uploaded"
        }

    pdf_path = os.path.join(JD_FOLDER, files[0])

    text = extract_text_from_pdf(pdf_path)

    skills = extract_jd_skills(text)

    return {
        "skills": skills
    }
    



# ─────────────────────────────────────────
# JD MATCHING ENDPOINTS
# ─────────────────────────────────────────

@app.post("/match-jd")
def match_jd_text(data: JDRequest):
    """
    Accept JD as pasted text (from LinkedIn, Naukri, Indeed, etc.),
    extract JD skills, then compare with uploaded resume skills.
    """

    # Get resume from uploads folder
    resume_files = os.listdir(UPLOAD_FOLDER)

    if not resume_files:
        return {
            "success": False,
            "message": "No resume uploaded. Please upload a resume first via /upload-resume"
        }

    resume_pdf_path = os.path.join(UPLOAD_FOLDER, resume_files[0])
    resume_text = extract_text_from_pdf(resume_pdf_path)

    # Extract skills from resume
    resume_skills = extract_skills(resume_text)

    # Extract skills from JD text
    jd_skills = extract_jd_skills(data.jd_text)

    if not jd_skills:
        return {
            "success": False,
            "message": "No recognizable skills found in the provided Job Description text."
        }

    # Run matcher
    match_result = match_jd(resume_skills, jd_skills)

    return {
        "success": True,
        "input_type": "text",
        "resume_file": resume_files[0],
        "resume_skills": {
            "categorized": resume_skills,
            "all": flatten_skills(resume_skills),
            "total": len(flatten_skills(resume_skills))
        },
        "jd_skills": {
            "categorized": jd_skills,
            "all": flatten_skills(jd_skills),
            "total": len(flatten_skills(jd_skills))
        },
        "match_result": match_result
    }


@app.post("/match-jd-pdf")
async def match_jd_pdf(file: UploadFile = File(...)):
    """
    Accept JD as a PDF upload, extract text + skills,
    then compare with uploaded resume skills.
    """

    # Save JD PDF
    jd_file_path = os.path.join(JD_FOLDER, file.filename)

    with open(jd_file_path, "wb") as buffer:
        buffer.write(await file.read())

    # Get resume from uploads folder
    resume_files = os.listdir(UPLOAD_FOLDER)

    if not resume_files:
        return {
            "success": False,
            "message": "No resume uploaded. Please upload a resume first via /upload-resume"
        }

    resume_pdf_path = os.path.join(UPLOAD_FOLDER, resume_files[0])
    resume_text = extract_text_from_pdf(resume_pdf_path)

    # Extract text from JD PDF
    jd_text = extract_text_from_jd_pdf(jd_file_path)

    if not jd_text.strip():
        return {
            "success": False,
            "message": "Could not extract text from the uploaded JD PDF."
        }

    # Extract skills from resume and JD
    resume_skills = extract_skills(resume_text)
    jd_skills = extract_jd_skills(jd_text)

    if not jd_skills:
        return {
            "success": False,
            "message": "No recognizable skills found in the uploaded JD PDF."
        }

    # Run matcher
    match_result = match_jd(resume_skills, jd_skills)

    return {
        "success": True,
        "input_type": "pdf",
        "jd_file": file.filename,
        "resume_file": resume_files[0],
        "resume_skills": {
            "categorized": resume_skills,
            "all": flatten_skills(resume_skills),
            "total": len(flatten_skills(resume_skills))
        },
        "jd_skills": {
            "categorized": jd_skills,
            "all": flatten_skills(jd_skills),
            "total": len(flatten_skills(jd_skills))
        },
        "match_result": match_result
    }


# ─────────────────────────────────────────
# AI FEEDBACK ENDPOINT
# ─────────────────────────────────────────

@app.post("/generate-feedback")
def generate_feedback(data: FeedbackRequest):
    """
    Call OpenRouter to generate AI-powered resume feedback.
    ATS scoring and skill matching are unaffected — this is purely additive.
    Returns pros, cons, and suggestions even if AI fails (graceful fallback).
    """
    result = generate_resume_feedback(
        resume_text    = data.resume_text,
        jd_text        = data.jd_text,
        ats_score      = data.ats_score,
        matched_skills = data.matched_skills,
        missing_skills = data.missing_skills
    )
    return result