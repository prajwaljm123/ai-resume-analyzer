import re

SKILL_CATEGORIES = {

    "programming_languages": [
        "java",
        "python",
        "c",
        "c++",
        "javascript",
        "typescript"
    ],

    "frontend": [
        "html",
        "css",
        "react",
        "angular",
        "vue"
    ],

    "backend": [
        "node.js",
        "express",
        "spring boot",
        "django",
        "flask"
    ],

    "database": [
        "mysql",
        "postgresql",
        "mongodb",
        "sqlite"
    ],

    "devops": [
        "git",
        "docker",
        "kubernetes",
        "jenkins"
    ],

    "cloud": [
        "aws",
        "azure",
        "gcp"
    ],

    "analytics": [
        "power bi",
        "tableau",
        "excel"
    ],

    "ai_ml": [
        "machine learning",
        "deep learning",
        "tensorflow",
        "pytorch"
    ],

    "cybersecurity": [
        "cybersecurity",
        "ethical hacking",
        "network security"
    ]
}


def extract_skills(text):

    text = text.lower()

    categorized_skills = {}

    for category, skills in SKILL_CATEGORIES.items():

        found_skills = []

        for skill in skills:

            pattern = r'\b' + re.escape(skill.lower()) + r'\b'

            if re.search(pattern, text):
                found_skills.append(skill)

        if found_skills:
            categorized_skills[category] = sorted(found_skills)

    return categorized_skills

def flatten_skills(categorized_skills):

    all_skills = []

    for skills in categorized_skills.values():
        all_skills.extend(skills)

    return sorted(set(all_skills))