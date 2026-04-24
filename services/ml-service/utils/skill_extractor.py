import json
import os
import re

# Load taxonomy file once
TAXONOMY_PATH = os.path.join(
    os.path.dirname(__file__),
    "skills_taxonomy.json"
)

with open(TAXONOMY_PATH, "r") as f:
    SKILL_TAXONOMY = json.load(f)


def normalize_text(text):
    """
    Lowercase + remove special characters for safer matching
    """
    return re.sub(r"[^a-zA-Z0-9+#. ]", " ", text.lower())


def extract_skills(text):
    """
    Extract canonical skills using taxonomy aliases
    """

    normalized_text = normalize_text(text)

    detected_skills = set()

    for canonical_skill, aliases in SKILL_TAXONOMY.items():
        for alias in aliases:

            # exact phrase match only (prevents 'c' matching inside 'cloud')
            pattern = r"\b" + re.escape(alias.lower()) + r"\b"

            if re.search(pattern, normalized_text):
                detected_skills.add(canonical_skill)
                break

    return sorted(list(detected_skills))