def compute_hybrid_match_score(
    exact_score,
    semantic_similarity_score,
    semantic_skill_matches,
    total_jd_skills
):
    """
    Combines exact matches, similarity-weighted semantic skill matches,
    and document-level similarity into a hybrid recruiter-style score.
    """

    if total_jd_skills == 0:
        return exact_score

    # NEW: weighted semantic skill contribution
    similarity_sum = sum(
        match["similarity"]
        for match in semantic_skill_matches
    )

    semantic_skill_score = (
        similarity_sum / total_jd_skills
    ) * 100

    # document similarity already 0–1 scale
    doc_score = semantic_similarity_score * 100

    hybrid_score = (
        0.5 * exact_score +
        0.3 * semantic_skill_score +
        0.2 * doc_score
    )

    return round(hybrid_score, 2)