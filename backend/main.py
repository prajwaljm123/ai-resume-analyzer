from fastapi import FastAPI, UploadFile, File
from pydantic import BaseModel
from parsers.resume_parser import extract_text_from_pdf

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

import os

app = FastAPI()

class JDRequest(BaseModel):
    jd_text: str

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
    
@app.post("/submit-jd")
def submit_jd(data: JDRequest):

    categorized_skills = extract_jd_skills(data.jd_text)

    all_skills = flatten_skills(categorized_skills)

    return {
        "skills": {
            "categorized": categorized_skills,
            "all": all_skills,
            "total_skills_found": len(all_skills)
        }
    }