from models.embedding_model import encode_text
from pipelines.vector_search import search_similar


def match_resume_to_job(job_description: str):
    """
    Matches job description against stored resume embeddings.
    Returns similarity results.
    """

    job_embedding = encode_text(job_description)

    results = search_similar(job_embedding)

    return results