import requests


OLLAMA_URL = "http://172.23.112.1:11434"
OLLAMA_MODEL = "llama3.2:latest"


def generate_assistant_response(
    resume_role,
    missing_skills,
    growth_roles,
    user_question
):
    """
    Uses local LLaMA model to answer career guidance questions
    based on resume intelligence extracted by ResumeLens.
    """

    prompt = f"""
You are ResumeLens, an AI career assistant helping candidates improve their resumes.

Candidate's Current Role:
{resume_role}

Missing Skills:
{missing_skills}

Suggested Growth Roles:
{growth_roles}

User Question:
{user_question}

Provide a helpful, realistic, and concise career suggestion.
Avoid generic advice.
Focus only on improvements relevant to the candidate profile.
"""

    try:
        response = requests.post(
            f"{OLLAMA_URL}/api/generate",
            json={
                "model": OLLAMA_MODEL,
                "prompt": prompt,
                "stream": False
            },
            timeout=30
        )

        if response.status_code == 200:
            return response.json()["response"].strip()

    except Exception:
        pass

    return "Assistant unavailable right now."