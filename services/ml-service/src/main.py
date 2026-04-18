from fastapi import FastAPI, UploadFile, File
import fitz  # PyMuPDF
from utils.skill_extractor import extract_skills
from models.embedding_model import encode_text
from pipelines.vector_store import (
    load_or_create_index,
    save_index,
    add_embedding
)
from pipelines.vector_search import search_similar

app = FastAPI()


def extract_text_from_pdf(file_bytes):
    text = ""
    page_count = 0

    with fitz.open(stream=file_bytes, filetype="pdf") as doc:
        page_count = len(doc)
        for page in doc:
            text += page.get_text()

    return text, page_count


@app.post("/upload-resume/")
async def upload_resume(file: UploadFile = File(...)):
    contents = await file.read()

    extracted_text, page_count = extract_text_from_pdf(contents)
    detected_skills = extract_skills(extracted_text)

    embedding_vector = encode_text(extracted_text)

    # Load FAISS index
    index = load_or_create_index()

    # Add embedding
    index = add_embedding(index, embedding_vector)

    # Save index
    save_index(index)

    return {
        "filename": file.filename,
        "page_count": page_count,
        "character_count": len(extracted_text),
        "word_count": len(extracted_text.split()),
        "detected_skills": detected_skills,
        "embedding_dimension": len(embedding_vector),
        "faiss_index_size": index.ntotal,
        "text_preview": extracted_text[:500],
    }

@app.post("/search-similar/")
async def search_similar_resumes(file: UploadFile = File(...)):
    contents = await file.read()
    extracted_text, _ = extract_text_from_pdf(contents)

    embedding_vector = encode_text(extracted_text)

    results = search_similar(embedding_vector)

    return results
