import requests


OLLAMA_URL = "http://172.23.112.1:11434"
OLLAMA_MODEL = "llama3.2:latest"


def llm_available():
    """
    Checks whether Ollama server AND model are available.
    Uses /api/tags endpoint.
    """

    try:
        response = requests.get(
            f"{OLLAMA_URL}/api/tags",
            timeout=3
        )

        if response.status_code != 200:
            return False

        models = response.json().get("models", [])

        return any(
            m["name"] == OLLAMA_MODEL
            for m in models
        )

    except Exception as e:
        print("Ollama availability check failed:", e)
        return False


def rule_based_explanation(
    semantic_score,
    skill_score,
    role_score,
    domain_score,
    matched_skills,
    missing_skills,
    resume_rank=None
):

    explanation_segments = []

    signals = {
        "semantic": semantic_score,
        "skills": skill_score,
        "role": role_score,
        "domain": domain_score
    }

    strongest_signal = max(signals, key=signals.get)

    if strongest_signal == "skills" and skill_score > 0.7:

        highlight = ", ".join(matched_skills[:4])

        explanation_segments.append(
            f"This profile stands out due to strong coverage of required technologies such as {highlight}"
        )

    elif strongest_signal == "semantic" and semantic_score > 0.6:

        explanation_segments.append(
            "The overall experience described in the resume closely reflects the responsibilities outlined in the job description"
        )

    elif strongest_signal == "role" and role_score > 0.7:

        explanation_segments.append(
            "The candidate’s professional role aligns directly with the target position requirements"
        )

    elif strongest_signal == "domain" and domain_score > 0.5:

        explanation_segments.append(
            "The candidate demonstrates meaningful exposure to the technical domain associated with this role"
        )

    else:

        explanation_segments.append(
            "The profile shows partial alignment with the expectations of the position but does not fully match the required specialization"
        )

    if skill_score == 0:

        explanation_segments.append(
            "Most of the core technical skills requested in the job description are currently not reflected in the resume"
        )

    elif skill_score < 0.5:

        explanation_segments.append(
            "Only limited overlap with the required technical stack is visible"
        )

    if role_score < 0.2:

        explanation_segments.append(
            "The candidate appears to be positioned in a different role track compared to the target position"
        )

    elif role_score < 0.6:

        explanation_segments.append(
            "The candidate’s experience suggests adjacency to the target role rather than direct specialization"
        )

    if 0.4 < domain_score < 0.7:

        explanation_segments.append(
            "Some relevant domain familiarity is present but deeper exposure would strengthen alignment further"
        )

    if missing_skills:

        preview = ", ".join(missing_skills[:3])

        explanation_segments.append(
            f"Strengthening experience in areas such as {preview} would significantly improve competitiveness for this role"
        )

    if resume_rank == 1:

        explanation_segments.append(
            "Compared with other retrieved candidates, this resume demonstrates the strongest overall alignment"
        )

    elif resume_rank == 2:

        explanation_segments.append(
            "Relative to other candidates evaluated, this resume shows moderate alignment with the job expectations"
        )

    elif resume_rank and resume_rank > 2:

        explanation_segments.append(
            "Compared with higher-ranked candidates, this profile currently shows weaker alignment with the role requirements"
        )

    return " ".join(explanation_segments)


def llm_explanation(
    matched_skills,
    missing_skills,
    semantic_score,
    role_score,
    domain_score,
    resume_rank
):

    matched_preview = ", ".join(matched_skills[:5]) if matched_skills else "None"
    missing_preview = ", ".join(missing_skills[:5]) if missing_skills else "None"

    prompt = f"""
    You are an AI career advisor explaining how well a resume matches a job role.

    Write a short professional explanation (2–3 sentences).

    Use ONLY the information below.

    Matched skills:
    {matched_preview}

    Missing skills:
    {missing_preview}

    Rules:

    - Mention ONLY skills listed above
    - Do NOT introduce new technologies
    - Do NOT assume project experience and mention only if available
    - Do NOT mention ranking numbers
    - Do NOT mention scores
    - Do NOT compare candidates
    - Do NOT say "candidate"
    - If missing skills exist → explain gaps clearly
    - If no missing skills exist → emphasize strong readiness
    - If several important skills are missing mention them → describe alignment as partial
    - Keep tone objective and realistic (not motivational)

    Return explanation text only.
    """

    try:

        response = requests.post(
            f"{OLLAMA_URL}/api/generate",
            json={
                "model": OLLAMA_MODEL,
                "prompt": prompt,
                "stream": False
            },
            timeout=90
        )

        if response.status_code == 200:

            print("Using LLM explanation (final controlled mode)")

            return response.json()["response"].strip()

    except Exception as e:

        print("LLM explanation error:", e)

    return None


def generate_ranking_explanation(
    semantic_score,
    skill_score,
    role_score,
    domain_score,
    matched_skills,
    missing_skills,
    resume_rank=None,
    resume_text=None,
    job_description=None
):

    if llm_available() and resume_text and job_description:

        explanation = llm_explanation(
            matched_skills,
            missing_skills,
            semantic_score,
            role_score,
            domain_score,
            resume_rank
        )

        if explanation:

            return {
                "text": explanation,
                "source": "llm"
            }

    print("Using fallback explanation (rule engine)")

    fallback_text = rule_based_explanation(
        semantic_score,
        skill_score,
        role_score,
        domain_score,
        matched_skills,
        missing_skills,
        resume_rank
    )

    return {
        "text": fallback_text,
        "source": "fallback"
    }