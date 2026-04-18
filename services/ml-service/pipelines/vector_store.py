import faiss
import numpy as np
import os

VECTOR_DIMENSION = 384
INDEX_PATH = "../../storage/vector_index/resume_index.faiss"


def load_or_create_index():
    """
    Loads FAISS index if exists, otherwise creates a new one.
    """
    if os.path.exists(INDEX_PATH):
        return faiss.read_index(INDEX_PATH)
    else:
        return faiss.IndexFlatL2(VECTOR_DIMENSION)


def save_index(index):
    """
    Saves FAISS index to disk.
    """
    faiss.write_index(index, INDEX_PATH)


def add_embedding(index, embedding_vector):
    """
    Adds embedding vector to FAISS index.
    """
    vector = np.array([embedding_vector]).astype("float32")
    index.add(vector)
    return index