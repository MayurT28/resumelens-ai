from utils.skill_extractor import extract_skills
from pipelines.semantic_expander import expand_skills
from pipelines.role_classifier import classify_resume_role
import json
import os
from pipelines.career_transition_advisor import suggest_role_transitions


CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))

REGISTRY_PATH = os.path.join(
    CURRENT_DIR,
    "../utils/role_skill_registry.json"
)


with open(REGISTRY_PATH, "r") as f:
    ROLE_SKILL_REGISTRY = json.load(f)


DOMAIN_SKILL_MAP = {

    "llm_systems": {
        "core": [
            "llm",
            "transformers",
            "rag pipelines",
            "prompt_engineering",
            "huggingface"
        ],
        "supporting": [
            "langchain",
            "langgraph",
            "embedding models",
            "fine tuning"
        ]
    },

    "ml_frameworks": {
        "core": [
            "pytorch",
            "tensorflow",
            "scikit-learn"
        ],
        "supporting": [
            "mlflow",
            "xgboost"
        ]
    },

    "data_stack": {
        "core": [
            "pandas",
            "numpy",
            "sql"
        ],
        "supporting": [
            "tableau",
            "powerbi"
        ]
    },

    "backend_engineering": {
        "core": [
            "fastapi",
            "flask",
            "django"
        ],
        "supporting": [
            "rest_api",
            "microservices"
        ]
    },

    "cloud_infrastructure": {
        "core": [
            "aws",
            "azure",
            "gcp"
        ],
        "supporting": [
            "docker",
            "kubernetes",
            "terraform",
            "ec2",
            "s3"
        ]
    },

    "frontend_engineering": {
        "core": [
            "react",
            "typescript"
        ],
        "supporting": [
            "css",
            "html",
            "tailwind",
            "javascript"
        ]
    },

    "mlops_stack": {
        "core": [
            "mlflow",
            "kubeflow"
        ],
        "supporting": [
            "airflow",
            "docker",
            "kubernetes"
        ]
    },

    "vector_search_stack": {
        "core": [
            "vector_database"
        ],
        "supporting": [
            "faiss",
            "pinecone",
            "weaviate"
        ]
    }

}

# --------------------------------------------------
# DOMAIN CLUSTER DEFINITIONS (EXTENSIBLE)
# --------------------------------------------------

DOMAIN_CLUSTERS = {

    "llm_systems": {
        "llm": 3,
        "transformers": 3,
        "prompt_engineering": 2,
        "rag pipelines": 3,
        "huggingface": 2
    },

    "ml_frameworks": {
        "pytorch": 3,
        "tensorflow": 3,
        "scikit-learn": 2,
        "machine_learning": 2
    },

    "data_stack": {
        "pandas": 2,
        "numpy": 2,
        "sql": 2,
        "spark": 3,
        "etl": 3
    },

    "backend_engineering": {
        "fastapi": 3,
        "flask": 2,
        "django": 3,
        "spring_boot": 3,
        "rest_api": 2,
        "microservices": 3
    },

    "cloud_infrastructure": {
        "aws": 3,
        "azure": 3,
        "gcp": 3,
        "docker": 2,
        "kubernetes": 3,
        "terraform": 3
    },

    "frontend_engineering": {
        "react": 3,
        "typescript": 2,
        "javascript": 2,
        "css": 1,
        "html": 1
    },

    "mlops_stack": {
        "mlflow": 3,
        "kubeflow": 3,
        "airflow": 2
    },

    "vector_search_stack": {
        "faiss": 3,
        "pinecone": 3,
        "milvus": 3,
        "weaviate": 2,
        "chroma": 2
    }
}


# --------------------------------------------------
# STRONG DOMAIN DETECTOR
# --------------------------------------------------

def detect_strong_domains(skills):

    strong_domains = []

    for domain, domain_skills in DOMAIN_SKILL_MAP.items():

        core = set(domain_skills.get("core", []))
        supporting = set(domain_skills.get("supporting", []))

        core_matches = core.intersection(skills)
        supporting_matches = supporting.intersection(skills)

        if len(core_matches) >= 1 or len(supporting_matches) >= 2:
            strong_domains.append(domain)

    return strong_domains


# --------------------------------------------------
# WEAK DOMAIN DETECTOR
# --------------------------------------------------

def detect_weak_domains(skills):

    weak_domains = []

    for domain, domain_skills in DOMAIN_SKILL_MAP.items():

        # Merge nested dict → single set
        if isinstance(domain_skills, dict):
            merged_skills = set()
            for category in domain_skills.values():
                merged_skills.update(category)
        else:
            merged_skills = set(domain_skills)

        overlap = merged_skills.intersection(skills)

        if len(overlap) == 0:
            weak_domains.append(domain)

    return weak_domains


# --------------------------------------------------
# ROLE-BASED SKILL GAP SUGGESTION
# --------------------------------------------------

def recommend_skill_upgrades(primary_role, resume_skills):

    role_data = ROLE_SKILL_REGISTRY.get(primary_role, {})

    recommended = []

    for category in role_data.values():

        for skill in category:

            if skill.replace(" ", "_") not in resume_skills:

                recommended.append(skill)

            if len(recommended) >= 5:
                return recommended

    return recommended


# --------------------------------------------------
# ROLE GROWTH PATH ENGINE
# --------------------------------------------------

def recommend_growth_roles(primary_role):

    growth_map = {

        "GenAI Engineer": [
            "LLM Engineer",
            "AI Platform Engineer",
            "MLOps Engineer"
        ],

        "Machine Learning Engineer": [
            "AI Architect",
            "Applied Scientist",
            "LLM Engineer"
        ],

        "Backend Engineer": [
            "Platform Engineer",
            "Cloud Engineer",
            "Solutions Architect"
        ],

        "Cloud Platform Engineer": [
            "Site Reliability Engineer",
            "Platform Engineer",
            "Cloud Security Engineer"
        ],

        "Data Engineer": [
            "Analytics Engineer",
            "ML Engineer",
            "Data Architect"
        ]
    }

    return growth_map.get(primary_role, [])


# --------------------------------------------------
# MAIN ANALYZER FUNCTION
# --------------------------------------------------

def analyze_resume_profile(resume_text):

    extracted_skills = expand_skills(
        extract_skills(resume_text)
    )

    extracted_skills = set(extracted_skills)

    role_result = classify_resume_role(resume_text)

    primary_role = role_result["primary_role"]

    secondary_roles = role_result["secondary_roles"]

    strong_domains = detect_strong_domains(extracted_skills)

    weak_domains = detect_weak_domains(extracted_skills)

    recommended_growth_roles = recommend_growth_roles(primary_role)

    recommended_skill_upgrades = recommend_skill_upgrades(
        primary_role,
        extracted_skills
    )

    transition_roles = suggest_role_transitions(
        set(extracted_skills),
        primary_role
    )

    return {

        "primary_role": primary_role,

        "secondary_roles": secondary_roles,

        "strong_domains": strong_domains,

        "weak_domains": weak_domains,

        "recommended_growth_roles": recommended_growth_roles,

        "recommended_skill_upgrades": recommended_skill_upgrades,

        "career_transition_options": transition_roles
    }