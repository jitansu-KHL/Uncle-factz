from pathlib import Path

LABELS = ["True", "Mostly True", "False", "Insufficient Evidence"]
LABEL2ID = {label: i for i, label in enumerate(LABELS)}
ID2LABEL = {i: label for label, i in LABEL2ID.items()}

BASE_DIR = Path(__file__).resolve().parent
BACKEND_DIR = BASE_DIR.parent
MODELS_DIR = BACKEND_DIR / "models"

# Small, CPU-friendly encoder. Swap to a larger model if you have a GPU.
DEFAULT_BASE_MODEL = "distilbert-base-uncased"

AGENT_KEYS = {
    "science": "Science Agent",
    "health": "Health Agent",
    "politics": "Politics Agent",
    "general": "General Agent",
}

AGENT_DOMAINS = {
    "science": "empirical science, physics, chemistry, biology, astronomy, earth science",
    "health": "medicine, public health, epidemiology, clinical guidelines",
    "politics": "legislation, government, public policy, economics, official records",
    "general": "logic, viral rumors, urban legends, timeline consistency",
}


def model_dir(agent_key: str) -> Path:
    return MODELS_DIR / agent_key
