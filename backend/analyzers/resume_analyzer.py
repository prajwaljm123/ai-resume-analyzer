def analyze_resume(contact, sections, skills):

    score = 0

    # Contact Information

    if contact.get("name"):
        score += 10

    if contact.get("email"):
        score += 10

    if contact.get("phone"):
        score += 10

    # Important Sections

    important_sections = [
        "profile",
        "skills",
        "experience",
        "projects",
        "education"
    ]

    for section in important_sections:
        if sections.get(section):
            score += 10

    # Skills Score

    total_skills = len(skills["all"])

    if total_skills >= 10:
        score += 15

    elif total_skills >= 5:
        score += 10

    elif total_skills >= 1:
        score += 5

    # Internship Score

    experience_text = sections.get("experience", "").lower()

    if "intern" in experience_text:
        score += 15

    return {
        "resume_score": min(score, 100)
    }