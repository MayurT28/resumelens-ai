import numpy as np
from pipelines.vector_store import load_or_create_index


def search_similar(embedding_vector, top_k=3):
    """
    Searches FAISS index for nearest neighbors.
    """
    index = load_or_create_index()

    if index.ntotal == 0:
        return []

    vector = np.array([embedding_vector]).astype("float32")

    distances, indices = index.search(vector, top_k)

    return {
        "indices": indices.tolist(),
        "distances": distances.tolist(),
        "total_vectors": index.ntotal,
    }