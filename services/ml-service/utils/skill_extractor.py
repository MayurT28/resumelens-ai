COMMON_SKILLS = [
    "python",
    "java",
    "c++",
    "machine learning",
    "deep learning",
    "data analysis",
    "sql",
    "pandas",
    "numpy",
    "tensorflow",
    "pytorch",
    "nlp",
    "react",
    "node.js",
    "docker",
    "aws",
    "fastapi",
    "flask",
    "git",
]


def extract_skills(text):
    text_lower = text.lower()
    detected_skills = []

    for skill in COMMON_SKILLS:
        if skill in text_lower:
            detected_skills.append(skill)

    return list(set(detected_skills))