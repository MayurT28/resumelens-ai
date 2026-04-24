from utils.skill_extractor import extract_skills
from pipelines.semantic_expander import expand_skills
from pipelines.role_classifier import classify_resume_role
import json
import os
from pipelines.role_mapper import normalize_role

CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))

REGISTRY_PATH = os.path.join(
    CURRENT_DIR,
    "../utils/role_skill_registry.json"
)


with open(REGISTRY_PATH, "r") as f:
    ROLE_SKILL_REGISTRY = json.load(f)


def get_role_skill_set(role):

    role_data = ROLE_SKILL_REGISTRY.get(role, {})

    skills = set()

    for category in role_data.values():
        skills.update(category)

    return skills


def compute_role_similarity(role_a, role_b):

    skills_a = get_role_skill_set(role_a)
    skills_b = get_role_skill_set(role_b)

    if not skills_a or not skills_b:
        return 0.5

    CORE_WEIGHT = 3
    STANDARD_WEIGHT = 1


    def weighted_similarity(skills_a, skills_b):

        intersection = skills_a.intersection(skills_b)
        union = skills_a.union(skills_b)

        score = 0

        for skill in intersection:

            if skill in [
                "llm",
                "transformers",
                "rag pipelines",
                "machine learning",
                "nlp",
                "microservices",
                "react",
                "data engineering",
                "kubernetes"
            ]:
                score += CORE_WEIGHT
            else:
                score += STANDARD_WEIGHT

        max_score = len(union) * CORE_WEIGHT

        return score / max_score

    similarity = weighted_similarity(skills_a, skills_b)

    return round(similarity, 3)


def compute_role_alignment_score(resume_text, job_description):
    """
    Compute role alignment using role-to-role similarity
    instead of JD skill overlap.
    """

    resume_role_data = classify_resume_role(resume_text)
    jd_role_data = classify_resume_role(job_description)

    resume_roles = set(
        [resume_role_data["primary_role"]] +
        resume_role_data.get("secondary_roles", [])
    )

    jd_roles = set(
        [jd_role_data["primary_role"]] +
        jd_role_data.get("secondary_roles", [])
    )

    # If any overlap → strong alignment
    if resume_roles.intersection(jd_roles):
        return 1.0

    # Otherwise compute registry similarity
    similarities = []

    for r_role in resume_roles:
        for j_role in jd_roles:
            similarities.append(
                compute_role_similarity(r_role, j_role)
            )

    if similarities:
        return round(max(similarities), 3)

    return 0.5