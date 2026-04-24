import json
import os
from pipelines.role_classifier import classify_resume_role


CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))

TRANSITION_PATH = os.path.join(
    CURRENT_DIR,
    "../utils/role_transition_registry.json"
)


with open(TRANSITION_PATH, "r") as f:
    ROLE_TRANSITIONS = json.load(f)


def predict_career_trajectory(resume_text):

    role_result = classify_resume_role(resume_text)

    primary_role = role_result["primary_role"]

    transition_data = ROLE_TRANSITIONS.get(primary_role, {})

    return {

        "current_role": primary_role,

        "next_roles": transition_data.get(
            "next_roles",
            []
        ),

        "adjacent_roles": transition_data.get(
            "adjacent_roles",
            []
        ),

        "long_term_roles": transition_data.get(
            "long_term_roles",
            []
        )
    }