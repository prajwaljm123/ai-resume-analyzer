from analyzers.skill_extractor import flatten_skills


def match_jd(resume_skills: dict, jd_skills: dict) -> dict:
    """
    Compare resume skills with JD skills and compute:
    - matched_skills (categorized + flat list)
    - missing_skills (categorized + flat list)
    - match_percentage
    - ats_score
    """

    matched_categorized = {}
    missing_categorized = {}

    # Collect all JD categories
    all_jd_categories = set(jd_skills.keys())
    all_resume_categories = set(resume_skills.keys())

    for category in all_jd_categories:

        jd_cat_skills = set(s.lower() for s in jd_skills.get(category, []))
        resume_cat_skills = set(s.lower() for s in resume_skills.get(category, []))

        matched = sorted(jd_cat_skills & resume_cat_skills)
        missing = sorted(jd_cat_skills - resume_cat_skills)

        if matched:
            matched_categorized[category] = matched

        if missing:
            missing_categorized[category] = missing

    # Flat lists
    all_jd_flat = flatten_skills(jd_skills)
    all_resume_flat = [s.lower() for s in flatten_skills(resume_skills)]

    matched_flat = sorted(set(s for s in all_jd_flat if s.lower() in all_resume_flat))
    missing_flat = sorted(set(s for s in all_jd_flat if s.lower() not in all_resume_flat))

    total_jd_skills = len(all_jd_flat)

    # --- Match Percentage ---
    if total_jd_skills == 0:
        match_percentage = 0.0
    else:
        match_percentage = round((len(matched_flat) / total_jd_skills) * 100, 2)

    # --- ATS Score (custom logic, no AI) ---
    ats_score = calculate_ats_score(
        match_percentage=match_percentage,
        matched_flat=matched_flat,
        missing_flat=missing_flat,
        jd_skills=jd_skills,
        resume_skills=resume_skills,
    )

    return {
        "matched_skills": {
            "categorized": matched_categorized,
            "all": matched_flat,
            "total_matched": len(matched_flat)
        },
        "missing_skills": {
            "categorized": missing_categorized,
            "all": missing_flat,
            "total_missing": len(missing_flat)
        },
        "total_jd_skills": total_jd_skills,
        "match_percentage": match_percentage,
        "ats_score": ats_score
    }


def calculate_ats_score(
    match_percentage: float,
    matched_flat: list,
    missing_flat: list,
    jd_skills: dict,
    resume_skills: dict
) -> int:
    """
    ATS score is calculated using custom developer logic:

    Breakdown (max 100):
    - Skill match percentage contribution  → up to 60 pts
    - Category coverage bonus              → up to 20 pts
    - Core skill presence bonus            → up to 10 pts
    - Penalty for too many missing skills  → up to -10 pts
    """

    score = 0

    # 1. Skill match percentage → 60 pts max
    score += round((match_percentage / 100) * 60)

    # 2. Category coverage bonus → 20 pts max
    # Reward if resume covers most JD categories
    jd_categories = set(jd_skills.keys())
    resume_categories = set(resume_skills.keys())
    covered_categories = jd_categories & resume_categories

    if len(jd_categories) > 0:
        category_coverage = len(covered_categories) / len(jd_categories)
        score += round(category_coverage * 20)

    # 3. Core skill presence bonus → 10 pts max
    # Bonus for having critical skill types present
    core_categories = ["programming_languages", "backend", "frontend", "database"]
    core_hits = sum(
        1 for cat in core_categories
        if cat in jd_skills and cat in resume_skills
    )
    score += min(core_hits * 3, 10)

    # 4. Penalty for high number of missing skills → -10 pts max
    total_jd = len(matched_flat) + len(missing_flat)
    if total_jd > 0:
        missing_ratio = len(missing_flat) / total_jd
        penalty = round(missing_ratio * 10)
        score -= penalty

    return max(0, min(score, 100))
