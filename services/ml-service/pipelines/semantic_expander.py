from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
import json
import os
from models.embedding_model import MODEL as model
from pathlib import Path


BASE_DIR = Path(__file__).resolve().parents[1]

TAXONOMY_PATH = BASE_DIR / "utils" / "skills_taxonomy.json"

with open(TAXONOMY_PATH, "r") as f:
    SKILL_TAXONOMY = json.load(f)


ALL_TAXONOMY_SKILLS = list(SKILL_TAXONOMY.keys())


taxonomy_embeddings = model.encode(ALL_TAXONOMY_SKILLS)


def expand_skills(input_skills, threshold=0.72):
    """
    Expands extracted skills using semantic similarity
    against taxonomy skill universe.

    Example:
    FastAPI → REST APIs
    EC2 → AWS
    Transformers → NLP
    """

    if not input_skills:
        return input_skills

    expanded_skills = set(input_skills)

    input_embeddings = model.encode(input_skills)

    for i, emb in enumerate(input_embeddings):

        similarities = cosine_similarity(
            [emb],
            taxonomy_embeddings
        )[0]

        for idx, score in enumerate(similarities):

            if score >= threshold:

                expanded_skills.add(
                    ALL_TAXONOMY_SKILLS[idx]
                )

    return list(expanded_skills)