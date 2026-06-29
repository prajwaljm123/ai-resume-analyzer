import re

SECTION_ALIASES = {

    "profile": [
        "profile",
        "professional summary",
        "summary",
        "career objective",
        "objective",
        "about me",
        "professional profile"
    ],

    "skills": [
        "skills",
        "technical skills",
        "technical expertise",
        "core skills",
        "core competencies",
        "competencies",
        "key skills",
        "technology stack",
        "tech stack",
        "technologies"
    ],

    "soft_skills": [
        "soft skills",
        "interpersonal skills",
        "behavioral skills",
        "personal skills"
    ],

    "experience": [
        "experience",
        "work experience",
        "professional experience",
        "employment history",
        "career history",
        "internship",
        "internships"
    ],

    "projects": [
        "projects",
        "academic projects",
        "personal projects",
        "key projects",
        "project experience",
        "project work"
    ],

    "education": [
        "education",
        "academic background",
        "academic qualification",
        "qualifications",
        "educational qualifications"
    ],

    "certifications": [
        "certifications",
        "certificates",
        "professional certifications",
        "courses",
        "training"
    ],

    "achievements": [
        "achievements",
        "accomplishments"
    ],

    "awards": [
        "awards",
        "honors",
        "recognitions"
    ],

    "leadership": [
        "leadership",
        "leadership experience",
        "positions of responsibility"
    ],

    "languages": [
        "languages",
        "language proficiency"
    ],

    "research": [
        "research",
        "research experience",
        "research work"
    ],

    "publications": [
        "publications",
        "research publications",
        "papers",
        "research papers"
    ],

    "volunteering": [
        "volunteering",
        "volunteer experience",
        "volunteer work",
        "community service"
    ],

    "interests": [
        "interests",
        "hobbies",
        "extracurricular activities"
    ],

    "references": [
        "references"
    ],

    "declaration": [
        "declaration"
    ],

    "contact": [
        "contact",
        "contact information"
    ]
}


def normalize(text):

    text = text.strip().lower()

    text = re.sub(r'[:\-]+$', '', text)

    text = re.sub(r'\s+', ' ', text)

    return text


def get_section_name(line):

    normalized_line = normalize(line)

    for section, aliases in SECTION_ALIASES.items():

        for alias in aliases:

            if normalized_line == normalize(alias):
                return section

    return None


def parse_sections(text):

    sections = {
        "header": []
    }

    current_section = "header"

    lines = text.split("\n")

    for line in lines:

        line = line.strip()

        if not line:
            continue

        # Remove standalone page numbers
        if re.fullmatch(r"\d+", line):
            continue

        detected_section = get_section_name(line)

        if detected_section:

            current_section = detected_section

            if current_section not in sections:
                sections[current_section] = []

            continue

        sections[current_section].append(line)

    result = {}

    for section, content in sections.items():

        cleaned_content = "\n".join(content).strip()

        if cleaned_content:
            result[section] = cleaned_content

    return result