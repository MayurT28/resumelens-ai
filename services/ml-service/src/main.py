from fastapi import FastAPI, UploadFile, File
import fitz  # PyMuPDF
from utils.skill_extractor import extract_skills

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

    return {
        "filename": file.filename,
        "page_count": page_count,
        "character_count": len(extracted_text),
        "word_count": len(extracted_text.split()),
        "detected_skills": detected_skills,
        "text_preview": extracted_text[:500],
    }

