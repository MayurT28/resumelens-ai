from utils.skill_extractor import extract_skills


def analyze_skill_gap(resume_text: str, job_description: str):
    """
    Compares resume skills with job description skills
    and returns matched and missing skills.
    """

    resume_skills = set(extract_skills(resume_text))
    job_skills = set(extract_skills(job_description))

    matched_skills = list(resume_skills.intersection(job_skills))
    missing_skills = list(job_skills.difference(resume_skills))

    match_score = 0

    if len(job_skills) > 0:
        match_score = int((len(matched_skills) / len(job_skills)) * 100)

    return {
        "match_score": match_score,
        "matched_skills": matched_skills,
        "missing_skills": missing_skills
    }