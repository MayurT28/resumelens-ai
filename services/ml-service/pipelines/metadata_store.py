import sqlite3
import os
from datetime import datetime
import json


# Get project root directory dynamically
CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))

PROJECT_ROOT = os.path.abspath(
    os.path.join(CURRENT_DIR, "../../../")
)

DB_FOLDER = os.path.join(
    PROJECT_ROOT,
    "storage",
    "vector_index"
)

# Ensure directory exists
os.makedirs(DB_FOLDER, exist_ok=True)

DB_PATH = os.path.join(DB_FOLDER, "metadata.db")


def get_connection():
    return sqlite3.connect(DB_PATH)


def initialize_database():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS resumes (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        filename TEXT,
        resume_text TEXT,
        predicted_role TEXT,
        skills TEXT,
        faiss_index INTEGER,
        created_at TEXT
    )
    """)

    conn.commit()
    conn.close()


def insert_resume_metadata(
    filename,
    resume_text,
    predicted_role,
    skills,
    faiss_index
):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
    INSERT INTO resumes (
        filename,
        resume_text,
        predicted_role,
        skills,
        faiss_index,
        created_at
    )
    VALUES (?, ?, ?, ?, ?, ?)
    """, (
        filename,
        resume_text,
        predicted_role,
        ", ".join(skills),
        faiss_index,
        datetime.utcnow().isoformat()
    ))

    conn.commit()
    conn.close()


def get_all_resumes():
    """
    Retrieve all stored resumes metadata ordered by FAISS index.
    """

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
    SELECT filename, resume_text, predicted_role, skills, faiss_index
    FROM resumes
    ORDER BY faiss_index ASC
    """)

    rows = cursor.fetchall()

    conn.close()

    resumes = []

    for row in rows:
        resumes.append({
            "filename": row[0],
            "resume_text": row[1],
            "predicted_role": row[2],
            "skills": row[3],
            "faiss_index": row[4]
        })

    return resumes
