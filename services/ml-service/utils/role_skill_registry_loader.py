import json
import os


def load_role_skill_registry():
    """
    Load role skill registry from utils directory.
    Centralized loader so all modules use the same source.
    """

    CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))

    REGISTRY_PATH = os.path.join(
        CURRENT_DIR,
        "role_skill_registry.json"
    )

    if not os.path.exists(REGISTRY_PATH):
        raise FileNotFoundError(
            f"Role skill registry not found at {REGISTRY_PATH}"
        )

    with open(REGISTRY_PATH, "r") as f:
        return json.load(f)