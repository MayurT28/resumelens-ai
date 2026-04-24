import faiss
import os
import numpy as np
import sqlite3
import faiss
from pipelines.metadata_store import get_all_resumes
from models.embedding_model import encode_text


CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))

PROJECT_ROOT = os.path.abspath(
    os.path.join(CURRENT_DIR, "../../../")
)

INDEX_PATH = os.path.join(
    PROJECT_ROOT,
    "storage",
    "vector_index",
    "resume_index.faiss"
)

DB_PATH = os.path.join(
    PROJECT_ROOT,
    "storage",
    "vector_index",
    "metadata.db"
)


def load_index():
    if not os.path.exists(INDEX_PATH):
        raise FileNotFoundError("FAISS index not found.")
    return faiss.read_index(INDEX_PATH)


def get_connection():
    return sqlite3.connect(DB_PATH)


def retrieve_similar_resumes(query_embedding, top_k=3):

    index = load_index()

    query_embedding = np.array([query_embedding]).astype("float32")

    distances, indices = index.search(query_embedding, top_k)

    conn = get_connection()
    cursor = conn.cursor()

    results = []

    for idx, dist in zip(indices[0], distances[0]):
        cursor.execute(
            "SELECT filename FROM resumes WHERE faiss_index=?",
            (int(idx),)
        )

        row = cursor.fetchone()

        if row:
            results.append({
                "filename": row[0],
                "distance": float(dist)
        })

    conn.close()

    return {
        "similar_resumes": results
    }

def rebuild_faiss_index():
    """
    Rebuild FAISS index from metadata DB and
    synchronize vector positions with SQLite.
    """

    import os
    import faiss
    import numpy as np
    import sqlite3

    from pipelines.metadata_store import get_all_resumes
    from models.embedding_model import encode_text

    # Resolve project root safely
    CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))

    PROJECT_ROOT = os.path.abspath(
        os.path.join(CURRENT_DIR, "../../../")
    )

    STORAGE_DIR = os.path.join(
        PROJECT_ROOT,
        "storage",
        "vector_index"
    )

    os.makedirs(STORAGE_DIR, exist_ok=True)

    INDEX_PATH = os.path.join(
        STORAGE_DIR,
        "resume_index.faiss"
    )

    DB_PATH = os.path.join(
        STORAGE_DIR,
        "metadata.db"
    )

    resumes = get_all_resumes()

    if not resumes:
        print("No resumes found.")
        return

    embeddings = []
    valid_resumes = []

    for resume in resumes:

        resume_text = resume.get("resume_text")

        if not resume_text:
            continue

        vector = encode_text(resume_text)

        embeddings.append(vector)
        valid_resumes.append(resume)

    if not embeddings:
        print("No embeddings generated.")
        return

    embeddings = np.array(embeddings).astype("float32")

    dimension = embeddings.shape[1]

    index = faiss.IndexFlatL2(dimension)
    index.add(embeddings)

    # Save FAISS index
    faiss.write_index(index, INDEX_PATH)

    # Sync SQLite faiss_index column
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    for new_idx, resume in enumerate(valid_resumes):

        cursor.execute(
            """
            UPDATE resumes
            SET faiss_index = ?
            WHERE filename = ?
            """,
            (new_idx, resume["filename"])
        )

    conn.commit()
    conn.close()

    print(f"FAISS index rebuilt successfully with {index.ntotal} resumes.")