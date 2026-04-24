from sentence_transformers import SentenceTransformer

# Single global instance
MODEL = SentenceTransformer("all-MiniLM-L6-v2")


def encode_text(text):
    return MODEL.encode(text)