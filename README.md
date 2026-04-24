![Python](https://img.shields.io/badge/Python-3.10-blue)
![FastAPI](https://img.shields.io/badge/FastAPI-Backend-green)
![React](https://img.shields.io/badge/React-Frontend-blue)
![FAISS](https://img.shields.io/badge/FAISS-Vector_Search-orange)
![Embeddings](https://img.shields.io/badge/Embeddings-SentenceTransformers-blueviolet)
![NLP](https://img.shields.io/badge/NLP-Semantic_Matching-purple)
![LLM](https://img.shields.io/badge/LLM-Ollama_Local-red)
![Project](https://img.shields.io/badge/Project-AI_Resume_Intelligence_Platform-black)
![Status](https://img.shields.io/badge/Status-Active-success)
![License](https://img.shields.io/badge/License-MIT-yellow)
# 📄 ResumeLens AI — Agentic Resume Intelligence Platform

**ResumeLens AI** is an intelligent resume analysis and candidate–job matching platform that uses semantic embeddings, hybrid scoring, vector search, and role intelligence pipelines to evaluate resumes against job descriptions.

Unlike traditional keyword-based ATS systems, ResumeLens performs **context-aware semantic matching**, **career trajectory prediction**, and **skill gap analysis** using modern NLP and vector similarity techniques.

----------------------------------------------------

# 🚀 Live Capabilities

ResumeLens supports multiple recruiter-style workflows:

## 1️⃣ AI Resume Matcher (Primary Feature)

Paste a job description → automatically selects the best matching resume from stored candidate profiles using:

- semantic similarity scoring
- skill overlap detection
- domain alignment analysis
- role classification matching
- hybrid scoring engine
- LLM explanation fallback system

----------------------------------------------------

## 2️⃣ Resume + Job Description Analyzer

Upload a resume + paste JD to generate:

- match score
- semantic similarity score
- hybrid match score
- matched skills
- missing skills
- semantic skill matches (example: AWS ↔ EC2)
- recommended skills to learn
- role alignment score

----------------------------------------------------

## 3️⃣ Resume Intelligence Report

Extracts structured career signals from resumes:

- primary role prediction
- secondary role predictions
- strong domain clusters
- weak domain clusters
- recommended growth roles
- skill upgrade roadmap
- career transition options

----------------------------------------------------

## 4️⃣ Career Trajectory Predictor

Forecasts career progression paths:

- current role detection
- adjacent roles
- next-step growth roles
- long-term leadership / research roles

----------------------------------------------------

# 🧠 Why ResumeLens AI is Different from ATS Systems

Traditional ATS platforms rely on keyword overlap.

ResumeLens instead uses:

✅ semantic embeddings  
✅ vector similarity search (FAISS)  
✅ role classification pipelines  
✅ hybrid scoring logic  
✅ domain-level reasoning  
✅ LLM-based explanation engine with fallback mode  

This produces significantly more accurate candidate–job alignment signals.

----------------------------------------------------

# 🏗️ System Architecture

React Frontend
↓
FastAPI Backend
↓
Resume Parser (pdfplumber)
↓
Skill Extraction Engine
↓
SentenceTransformer Embeddings
↓
FAISS Vector Index
↓
Hybrid Matching Engine
↓
LLM Explanation Layer (Ollama)

----------------------------------------------------

# ⚙️ Core AI Pipelines

ResumeLens includes multiple intelligent pipelines:

## Resume Role Classification Pipeline

Predicts:

- primary role
- secondary roles
- role confidence scores

Uses embedding similarity between resume content and structured role skill registries.

----------------------------------------------------

## Semantic Skill Matching Engine

Detects equivalent technologies such as:

AWS ↔ EC2
Transformers ↔ HuggingFace
FastAPI ↔ Flask


Improves matching beyond keyword overlap.

----------------------------------------------------

## Hybrid Resume–JD Match Scoring Engine

Combines:

exact skill match score
+
semantic similarity score
+
semantic skill matches


Produces a robust alignment metric.

-------------------------------------------------

## Domain Intelligence Analyzer

Clusters resume signals into domains:

LLM Systems
Backend Engineering
Cloud Infrastructure
ML Frameworks
Vector Search Stack


Identifies strengths and improvement areas.

-------------------------------------------------

## Career Trajectory Predictor

Estimates:

next roles
adjacent roles
long-term progression paths


Based on detected skill distribution and role similarity embeddings.

-------------------------------------------------

## Resume Improvement Suggestion Engine

Generates:


missing skills
recommended upgrades
growth-role readiness suggestions


Used to create structured learning roadmaps.

-------------------------------------------------

## LLM Explanation Engine (Fallback Enabled)

ResumeLens uses local LLM inference via:


Ollama + LLaMA


If unavailable:


rule-based explanation engine activates automatically


Ensures deterministic behavior without cloud dependency.

-------------------------------------------------

# 🧰 Tech Stack

## Backend

- FastAPI
- Python
- FAISS (Vector Search)
- SentenceTransformers
- NumPy
- Scikit-learn
- pdfplumber
- SQLite

-------------------------------------------------

## Frontend

- React
- TailwindCSS
- Axios

-------------------------------------------------

## AI Components

- Semantic Embeddings (SentenceTransformers)
- Hybrid Matching Engine
- Role Classification Model
- Skill Extraction Engine
- Domain Intelligence Analyzer
- Career Trajectory Predictor
- Semantic Skill Matcher
- LLM Explanation Layer (Ollama)

-------------------------------------------------

# 📂 Project Structure


resumelens-ai/
│
├── services/
│ └── ml-service/
│ ├── src/
│ ├── pipelines/
│ ├── models/
│ ├── utils/
│ └── storage/
│
├── resumelens-ui/
│
└── README.md


-------------------------------------------------

# ▶️ Running the Project Locally

## Backend Setup


cd services/ml-service
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
uvicorn src.main:app --reload


Server starts at:


http://127.0.0.1:8000


-------------------------------------------------

## Frontend Setup


cd resumelens-ui
npm install
npm run dev


Frontend runs at:


http://localhost:5173


-------------------------------------------------

# 🧪 Example Use Cases

ResumeLens supports:

- recruiter candidate ranking workflows
- skill gap detection
- role readiness evaluation
- career transition planning
- semantic resume search
- JD–resume compatibility scoring
- resume intelligence extraction

-----------------------------------------------

# 📊 Example Matching Signals Generated

ResumeLens computes:

match_score
semantic_similarity_score
hybrid_match_score
role_alignment
matched_skills
missing_skills
semantic_skill_matches
recommended_skills

These signals provide structured explainability for hiring decisions.

---------------------------------------------------------

# 🔐 Offline-First LLM Support

ResumeLens supports:

Ollama local inference

Benefits:

- privacy-safe processing
- no API costs
- deterministic fallback mode
- reproducible explanations

----------------------------------------------------

# 🧩 Future Improvements (Planned)

- recruiter dashboard view
- resume clustering visualization
- experience-level estimation
- multi-candidate comparison tables
- Docker deployment support
- AWS production deployment pipeline

----------------------------------------------------

# 👨‍💻 Author

**Mayur Tonge**

GitHub:
https://github.com/MayurT28


----------------------------------------------------

# ⭐ Why This Project Matters

ResumeLens demonstrates:

✔ semantic search engineering  
✔ vector database usage (FAISS)  
✔ hybrid scoring systems  
✔ explainable AI pipelines  
✔ role classification modeling  
✔ career trajectory prediction  
✔ LLM integration with fallback design  
✔ full-stack AI system architecture  

Designed as a recruiter-grade intelligent resume evaluation platform rather than a keyword-matching ATS clone.