from models.embedding_model import MODEL
from sklearn.metrics.pairwise import cosine_similarity
import json
import os


BASE_DIR = os.path.dirname(os.path.dirname(__file__))

ROLE_TARGETS_PATH = os.path.join(
    BASE_DIR,
    "utils",
    "role_skill_targets.json"
)


with open(ROLE_TARGETS_PATH, "r") as f:
    ROLE_SKILL_TARGETS = json.load(f)


def recommend_skills_for_role(
    primary_role,
    resume_text,
    top_n=5
):

    role_targets = ROLE_SKILL_TARGETS.get(primary_role, [])

    if not role_targets:
        return []

    resume_embedding = MODEL.encode([resume_text])

    target_embeddings = MODEL.encode(role_targets)

    recommendations = []

    for i, target_skill in enumerate(role_targets):

        similarity = cosine_similarity(
            [target_embeddings[i]],
            resume_embedding
        )[0][0]

        if similarity < 0.70:
            recommendations.append(target_skill)

    return recommendations[:top_n]