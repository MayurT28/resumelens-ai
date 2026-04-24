from collections import defaultdict
from models.embedding_model import MODEL
from sklearn.metrics.pairwise import cosine_similarity


def generate_recommended_skills(
    missing_skills,
    semantic_skill_matches,
    jd_skills,
    top_n=3
):
    """
    Generates role-aware recommendations using:

    1. similarity to resume skills
    2. similarity to other JD skills
    3. JD presence importance
    """

    recommendation_scores = defaultdict(float)

    # Resume proximity signal
    for match in semantic_skill_matches:
        jd_skill = match["jd_skill"]

        if jd_skill in missing_skills:
            recommendation_scores[jd_skill] += match["similarity"]

    # JD cluster similarity signal
    if jd_skills:

        jd_embeddings = MODEL.encode(jd_skills)
        missing_embeddings = MODEL.encode(missing_skills)

        for i, missing_skill in enumerate(missing_skills):

            similarities = cosine_similarity(
                [missing_embeddings[i]],
                jd_embeddings
            )[0]

            cluster_score = sum(similarities) / len(similarities)

            recommendation_scores[missing_skill] += cluster_score * 0.5

    # JD presence importance
    for skill in missing_skills:
        recommendation_scores[skill] += 0.5

    ranked = sorted(
        recommendation_scores.items(),
        key=lambda x: x[1],
        reverse=True
    )

    return [skill for skill, _ in ranked[:top_n]]