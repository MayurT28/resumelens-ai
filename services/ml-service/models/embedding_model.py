from sentence_transformers import SentenceTransformer

# Load embedding model once globally
embedding_model = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2")


def encode_text(text: str):
    """
    Converts input text into semantic embedding vector.
    """
    return embedding_model.encode(text)