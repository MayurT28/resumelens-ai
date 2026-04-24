from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np
from models.embedding_model import MODEL as model

# Load lightweight semantic embedding model



def compute_semantic_similarity(text_a: str, text_b: str) -> float:
    """
    Computes cosine similarity between two text blocks.
    Returns similarity score between 0 and 1.
    """

    if not text_a.strip() or not text_b.strip():
        return 0.0

    embeddings = model.encode([text_a, text_b])

    similarity = cosine_similarity(
        [embeddings[0]],
        [embeddings[1]]
    )[0][0]

    return float(round(similarity, 4))


def compute_resume_jd_similarity(resume_text: str, jd_text: str) -> dict:
    """
    Computes semantic alignment score between resume and job description.
    """

    score = compute_semantic_similarity(resume_text, jd_text)

    return {
        "semantic_similarity_score": score
    }