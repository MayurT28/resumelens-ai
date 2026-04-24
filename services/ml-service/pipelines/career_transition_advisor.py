from utils.role_skill_registry_loader import load_role_skill_registry

ROLE_SKILL_REGISTRY = load_role_skill_registry()


CORE_SKILLS = {
    "machine_learning",
    "nlp",
    "transformers",
    "llm",
    "microservices",
    "kubernetes",
    "react",
    "data_engineering",
    "pytorch",
    "tensorflow"
}


def evaluate_transition_strength(resume_skills, target_role):

    role_data = ROLE_SKILL_REGISTRY.get(target_role, {})

    role_skills = set()

    for category in role_data.values():
        role_skills.update(category)

    overlap = role_skills.intersection(resume_skills)

    strong_overlap = overlap.intersection(CORE_SKILLS)

    return len(overlap), len(strong_overlap), overlap


def suggest_role_transitions(resume_skills, primary_role):

    suggestions = []

    for role in ROLE_SKILL_REGISTRY.keys():

        if role == primary_role:
            continue

        total_overlap, strong_overlap, overlap_skills = \
            evaluate_transition_strength(resume_skills, role)

        if total_overlap >= 3 or strong_overlap >= 2:

            suggestions.append({
                "role": role,
                "supporting_skills": list(overlap_skills)[:5],
                "confidence": "strong"
            })

    return suggestions