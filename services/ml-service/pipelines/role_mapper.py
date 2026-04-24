ROLE_NORMALIZATION_MAP = {

    "Java Developer": "Backend Engineer",
    "Python Developer": "Backend Engineer",
    "Software Engineer": "Full Stack Developer",
    "Digital Engineer": "Backend Engineer",
    "Application Developer": "Backend Engineer",

    "AI Engineer": "GenAI Engineer",
    "LLM Engineer": "GenAI Engineer",

    "ML Engineer": "Machine Learning Engineer",

    "Cloud Developer": "Cloud Engineer",

    "Frontend Developer": "Frontend Engineer",

    "DevOps Specialist": "DevOps Engineer",

}


def normalize_role(role):

    return ROLE_NORMALIZATION_MAP.get(role, role)