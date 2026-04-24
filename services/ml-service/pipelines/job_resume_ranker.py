import numpy as np
from models.embedding_model import encode_text
from pipelines.resume_retriever import load_index
from pipelines.metadata_store import get_all_resumes
from utils.skill_extractor import extract_skills
from pipelines.semantic_expander import expand_skills
from pipelines.role_classifier import classify_resume_role
from pipelines.semantic_matcher import compute_resume_jd_similarity
from pipelines.skill_equivalence_matcher import find_semantic_skill_matches
from pipelines.learning_roadmap_generator import generate_learning_roadmap
from pipelines.role_similarity_engine import compute_role_alignment_score
from pipelines.ranking_explainer import generate_ranking_explanation


def compute_skill_gap(resume_text, job_description):

    resume_skills = expand_skills(
        extract_skills(resume_text)
    )

    jd_skills = expand_skills(
        extract_skills(job_description)
    )

    matched = list(
        set(resume_skills).intersection(set(jd_skills))
    )

    missing = list(
        set(jd_skills) - set(resume_skills)
    )

    return matched, missing


def normalize_score(distance):
    similarity = 1 / (1 + distance)
    return round(similarity * 100, 2)


def compute_skill_overlap_score(resume_text, job_description):

    resume_skills = expand_skills(
        extract_skills(resume_text)
    )

    jd_skills = expand_skills(
        extract_skills(job_description)
    )

    if not jd_skills:
        return 0

    exact_matches = set(resume_skills).intersection(set(jd_skills))

    semantic_matches = find_semantic_skill_matches(
        resume_skills,
        jd_skills
    )

    semantic_match_count = len({
        match["jd_skill"] for match in semantic_matches
    })

    total_matches = len(exact_matches) + semantic_match_count

    return min(total_matches / len(jd_skills), 1.0)


def compute_domain_alignment_score(resume_text, job_description):

    resume_lower = resume_text.lower()
    jd_lower = job_description.lower()

    domain_keywords = [
        "nlp",
        "llm",
        "transformers",
        "analytics",
        "backend",
        "cloud",
        "deployment",
        "machine learning",
        "data engineering"
    ]

    matches = sum(
        1 for keyword in domain_keywords
        if keyword in resume_lower and keyword in jd_lower
    )

    return matches / len(domain_keywords)


def rank_resumes_for_job(job_description, top_k=5):

    jd_embedding = encode_text(job_description)

    index = load_index()

    if index.ntotal == 0:
        return {"ranked_resumes": []}

    distances, indices = index.search(
        np.array([jd_embedding]).astype("float32"),
        min(top_k, index.ntotal)
    )

    resumes = get_all_resumes()

    ranked_results = []

    for rank, idx in enumerate(indices[0]):

        if idx == -1:
            continue

        if idx >= len(resumes):
            continue

        matching_resume = resumes[idx]

        filename = matching_resume["filename"]
        resume_text = matching_resume["resume_text"]

        semantic_score = compute_resume_jd_similarity(
            resume_text,
            job_description
        )["semantic_similarity_score"]

        skill_score = compute_skill_overlap_score(
            resume_text,
            job_description
        )

        role_score = compute_role_alignment_score(
            resume_text,
            job_description
        )

        domain_score = compute_domain_alignment_score(
            resume_text,
            job_description
        )

        matched_skills, missing_skills = compute_skill_gap(
            resume_text,
            job_description
        )

        recommended_skills = generate_learning_roadmap(
            resume_text,
            job_description
        )

        final_score = round(
            (
                semantic_score * 0.40
                + skill_score * 0.30
                + role_score * 0.20
                + domain_score * 0.10
            ) * 100,
            2
        )

        explanation_result = generate_ranking_explanation(
            semantic_score,
            skill_score,
            role_score,
            domain_score,
            matched_skills,
            missing_skills,
            resume_rank=rank + 1,
            resume_text=resume_text,
            job_description=job_description
        )

        ranked_results.append({

            "filename": filename,

            "final_score": final_score,

            "score_breakdown": {
                "semantic_similarity": round(semantic_score, 3),
                "skill_overlap": round(skill_score, 3),
                "role_alignment": round(role_score, 3),
                "domain_alignment": round(domain_score, 3)
            },

            "matched_skills": matched_skills,

            "missing_skills": missing_skills,

            "recommended_skills_to_learn": recommended_skills,

            "ranking_explanation": explanation_result["text"],
            "explanation_source": explanation_result["source"]
        })

    return {
        "ranked_resumes": ranked_results
    }