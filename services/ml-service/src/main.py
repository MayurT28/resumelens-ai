from fastapi import FastAPI, UploadFile, File, Form
import fitz  # PyMuPDF
from utils.skill_extractor import extract_skills
from models.embedding_model import encode_text
from pipelines.vector_store import (load_or_create_index, save_index, add_embedding)
from pipelines.vector_search import search_similar
from pipelines.job_matcher import match_resume_to_job
from pipelines.skill_gap_analyzer import analyze_skill_gap
from pipelines.semantic_matcher import compute_resume_jd_similarity
from pipelines.semantic_skill_matcher import find_semantic_skill_matches
from pipelines.hybrid_scorer import compute_hybrid_match_score
from pipelines.semantic_expander import expand_skills
from pipelines.recommendation_engine import generate_recommended_skills
from pipelines.role_classifier import classify_resume_role
from pipelines.role_skill_recommender import recommend_skills_for_role
from pipelines.metadata_store import initialize_database
from pipelines.metadata_store import insert_resume_metadata
from pipelines.resume_retriever import retrieve_similar_resumes
from pipelines.job_resume_ranker import rank_resumes_for_job
from pipelines.resume_profile_analyzer import analyze_resume_profile
from pipelines.role_similarity_engine import compute_role_alignment_score
from pipelines.role_mapper import normalize_role
from pipelines.resume_profile_analyzer import analyze_resume_profile
from pipelines.career_trajectory_predictor import (predict_career_trajectory)
from fastapi.middleware.cors import CORSMiddleware
from fastapi import UploadFile, File
import shutil
from pathlib import Path
from pipelines.resume_retriever import rebuild_faiss_index
from pipelines.role_classifier import classify_resume_role
import pdfplumber
from pipelines.metadata_store import get_all_resumes

app = FastAPI()
initialize_database()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

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

    # Add embedding and get position
    index = add_embedding(index, embedding_vector)

    faiss_position = index.ntotal - 1

    # Predict role
    role_prediction = classify_resume_role(extracted_text)["primary_role"]

    # Store metadata in SQLite
    insert_resume_metadata(
        filename=file.filename,
        resume_text=extracted_text,
        predicted_role=role_prediction,
        skills=detected_skills,
        faiss_index=faiss_position
    )

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

@app.post("/match-job/")
async def match_job_description(job_description: str):
    """
    Matches a job description against stored resumes.
    """

    results = match_resume_to_job(job_description)

    return results

@app.post("/analyze-match/")
async def analyze_resume_job_match(
    file: UploadFile = File(...),
    job_description: str = Form(...)
):
    """
    Upload resume + job description together
    and return match analysis + semantic similarity score.
    """

    contents = await file.read()
    extracted_text, _ = extract_text_from_pdf(contents)

    # Skill gap analysis
    analysis = analyze_skill_gap(extracted_text, job_description)
    resume_role = normalize_role(
        classify_resume_role(extracted_text)["primary_role"]
    )

    jd_role = normalize_role(
        classify_resume_role(job_description)["primary_role"]
    )

    analysis["resume_role"] = resume_role
    analysis["jd_role"] = jd_role

    role_alignment = compute_role_alignment_score(
        extracted_text,
        job_description
    )

    analysis["role_alignment"] = role_alignment

    # Document-level semantic similarity
    semantic_result = compute_resume_jd_similarity(
        extracted_text,
        job_description
    )

    analysis["semantic_similarity_score"] = semantic_result[
        "semantic_similarity_score"
    ]

    # Expanded skills for deeper comparison
    resume_skills = expand_skills(
        extract_skills(extracted_text)
    )

    jd_skills = expand_skills(
        extract_skills(job_description)
    )

    # Semantic skill matching
    semantic_skill_matches = find_semantic_skill_matches(
        resume_skills,
        jd_skills
    )

    analysis["semantic_skill_matches"] = semantic_skill_matches

    # Hybrid scoring
    total_jd_skills = (
        len(analysis["matched_skills"])
        + len(analysis["missing_skills"])
    )

    hybrid_score = compute_hybrid_match_score(
        exact_score=analysis["match_score"],
        semantic_similarity_score=semantic_result[
            "semantic_similarity_score"
        ],
        semantic_skill_matches=semantic_skill_matches,
        total_jd_skills=total_jd_skills
    )

    analysis["hybrid_match_score"] = hybrid_score

    # Recommended skills engine
    recommended_skills = generate_recommended_skills(
        missing_skills=analysis["missing_skills"],
        semantic_skill_matches=semantic_skill_matches,
        jd_skills=jd_skills
    )

    analysis["recommended_skills"] = recommended_skills

    return analysis

@app.post("/classify-role/")
async def classify_role(file: UploadFile = File(...)):
    """
    Classifies resume into primary + secondary roles
    and recommends next skills for the detected role.
    """

    contents = await file.read()
    extracted_text, _ = extract_text_from_pdf(contents)

    role_prediction = classify_resume_role(extracted_text)

    detected_skills = extract_skills(extracted_text)

    recommended_skills = recommend_skills_for_role(
    primary_role=role_prediction["primary_role"],
    resume_text=extracted_text
    )

    role_prediction["recommended_skills_for_role"] = recommended_skills

    return role_prediction

@app.post("/top-matching-resumes/")
async def top_matching_resumes(file: UploadFile = File(...)):
    """
    Upload a resume and retrieve most similar resumes
    previously stored in ResumeLens.
    """

    contents = await file.read()

    extracted_text, _ = extract_text_from_pdf(contents)

    embedding_vector = encode_text(extracted_text)

    results = retrieve_similar_resumes(embedding_vector)

    return results

@app.post("/rank-resumes-for-job/")
async def rank_resumes(job_description: str):
    """
    Rank stored resumes based on job description similarity.
    """

    results = rank_resumes_for_job(job_description)

    return results

@app.post("/analyze-resume-profile/")
async def analyze_resume_profile_endpoint(
    file: UploadFile = File(...)
):

    contents = await file.read()

    extracted_text, _ = extract_text_from_pdf(contents)

    profile = analyze_resume_profile(extracted_text)

    return profile

@app.post("/analyze-profile/")
async def analyze_profile(file: UploadFile = File(...)):

    contents = await file.read()

    extracted_text, _ = extract_text_from_pdf(contents)

    result = analyze_resume_profile(extracted_text)

    return result

@app.post("/career-trajectory/")
async def career_trajectory(
    file: UploadFile = File(...)
):

    contents = await file.read()

    extracted_text, _ = extract_text_from_pdf(
        contents
    )

    result = predict_career_trajectory(
        extracted_text
    )

    return result

@app.post("/upload-resume/")
async def upload_resume(file: UploadFile = File(...)):

    # Extract text from PDF
    with pdfplumber.open(file.file) as pdf:
        resume_text = "\n".join(
            page.extract_text() or ""
            for page in pdf.pages
        )

    predicted_role = classify_resume_role(resume_text)["primary_role"]

    skills = extract_skills(resume_text)

    # Temporary index placeholder (updated later)
    faiss_index = -1

    insert_resume_metadata(
        file.filename,
        resume_text,
        predicted_role,
        skills,
        faiss_index
    )

    rebuild_faiss_index()

    return {
        "message": "Resume uploaded and indexed successfully"
    }

@app.get("/list-resumes/")
def list_resumes():
    resumes = get_all_resumes()

    return {
        "resumes": [
            {
                "filename": r["filename"],
                "predicted_role": r["predicted_role"]
            }
            for r in resumes
        ]
    }