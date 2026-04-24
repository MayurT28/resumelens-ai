import json
import os
from models.embedding_model import MODEL
from sklearn.metrics.pairwise import cosine_similarity


BASE_DIR = os.path.dirname(os.path.dirname(__file__))

ROLE_REGISTRY_PATH = os.path.join(
    BASE_DIR,
    "utils",
    "role_registry.json"
)


with open(ROLE_REGISTRY_PATH, "r") as f:
    ROLE_REGISTRY = json.load(f)


def flatten_roles(role_registry):
    """
    Converts hierarchical registry into flat structure:
    role_name -> skill list
    """

    flat_roles = {}

    for domain in role_registry:
        for role, skills in role_registry[domain].items():
            flat_roles[role] = skills

    return flat_roles


FLAT_ROLE_MAP = flatten_roles(ROLE_REGISTRY)


def classify_resume_role(resume_text, threshold=0.40):
    """
    Classifies resume into primary + secondary roles
    using embedding similarity.
    """

    role_names = list(FLAT_ROLE_MAP.keys())

    role_skill_strings = [
        " ".join(FLAT_ROLE_MAP[role])
        for role in role_names
    ]

    role_embeddings = MODEL.encode(role_skill_strings)

    resume_embedding = MODEL.encode([resume_text])[0]

    similarities = cosine_similarity(
        [resume_embedding],
        role_embeddings
    )[0]

    role_scores = dict(
        zip(role_names, similarities)
    )

    sorted_roles = sorted(
        role_scores.items(),
        key=lambda x: x[1],
        reverse=True
    )

    primary_role = sorted_roles[0][0]

    secondary_roles = [
        role
        for role, score in sorted_roles[1:]
        if score >= threshold
    ][:3]

    confidence_scores = {
        role: round(float(score), 3)
        for role, score in sorted_roles[:3]
    }

    return {
        "primary_role": primary_role,
        "secondary_roles": secondary_roles,
        "confidence_scores": confidence_scores
    }