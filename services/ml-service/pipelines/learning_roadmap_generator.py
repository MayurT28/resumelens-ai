from utils.skill_extractor import extract_skills
from pipelines.semantic_expander import expand_skills


def generate_learning_roadmap(resume_text, job_description, top_n=5):
    """
    Suggest most valuable skills to learn based on JD mismatch.
    """

    resume_skills = expand_skills(
        extract_skills(resume_text)
    )

    jd_skills = expand_skills(
        extract_skills(job_description)
    )

    missing_skills = list(
        set(jd_skills) - set(resume_skills)
    )

    # Return top N missing skills
    return missing_skills[:top_n]