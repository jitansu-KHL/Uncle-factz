"""
Load and run per-agent specialist classifiers.

Each checkpoint under backend/models/<agent_key>/ is a DistilBERT
sequence classifier trained for that domain.
"""

from __future__ import annotations

import json
import threading
from functools import lru_cache
from typing import List, Optional

from backend.training.config import (
    AGENT_KEYS,
    ID2LABEL,
    LABELS,
    model_dir,
)

_LOCK = threading.Lock()
_CACHE: dict = {}


def agent_name_to_key(agent_name: str) -> Optional[str]:
    for key, name in AGENT_KEYS.items():
        if name == agent_name or key in agent_name.lower():
            return key
    lowered = agent_name.lower()
    for key in AGENT_KEYS:
        if key in lowered:
            return key
    return None


def specialist_available(agent_name: str) -> bool:
    key = agent_name_to_key(agent_name)
    if not key:
        return False
    path = model_dir(key)
    return (path / "config.json").exists()


def list_ready_specialists() -> List[str]:
    return [name for name in AGENT_KEYS.values() if specialist_available(name)]


def _encode(claim: str, evidence_sources: Optional[List[dict]]) -> str:
    snippets = []
    if evidence_sources:
        for src in evidence_sources:
            title = src.get("title", "")
            snippet = src.get("snippet", "")
            snippets.append(f"{title}. {snippet}".strip())
    evidence = " ".join(snippets)[:1200] if snippets else "none"
    return f"claim: {claim.strip()} evidence: {evidence}"


@lru_cache(maxsize=8)
def _load_bundle(agent_key: str):
    import torch
    from transformers import AutoModelForSequenceClassification, AutoTokenizer

    path = str(model_dir(agent_key))
    tokenizer = AutoTokenizer.from_pretrained(path)
    model = AutoModelForSequenceClassification.from_pretrained(path)
    model.eval()
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    model.to(device)
    meta_path = model_dir(agent_key) / "meta.json"
    meta = json.loads(meta_path.read_text(encoding="utf-8")) if meta_path.exists() else {}
    return tokenizer, model, device, meta


def predict_verdict(
    agent_name: str,
    claim: str,
    evidence_sources: Optional[List[dict]] = None,
) -> Optional[dict]:
    """
    Returns verdict/confidence from the agent's trained classifier, or None
    if that specialist has not been trained yet.
    """
    key = agent_name_to_key(agent_name)
    if not key or not specialist_available(agent_name):
        return None

    try:
        import torch
        import torch.nn.functional as F
    except ImportError:
        return None

    with _LOCK:
        tokenizer, model, device, meta = _load_bundle(key)

    text = _encode(claim, evidence_sources)
    encoded = tokenizer(
        text,
        truncation=True,
        padding=True,
        max_length=256,
        return_tensors="pt",
    )
    encoded = {k: v.to(device) for k, v in encoded.items()}

    with torch.no_grad():
        logits = model(**encoded).logits
        probs = F.softmax(logits, dim=-1)[0]

    pred_id = int(torch.argmax(probs).item())
    confidence = float(probs[pred_id].item())
    # Calibrate: never report 1.0 from a small model
    confidence = max(0.35, min(0.95, confidence))

    id2label = getattr(model.config, "id2label", ID2LABEL) or ID2LABEL
    verdict = id2label.get(pred_id, id2label.get(str(pred_id), LABELS[pred_id]))
    if verdict not in LABELS:
        verdict = LABELS[pred_id] if pred_id < len(LABELS) else "Insufficient Evidence"

    return {
        "verdict": verdict,
        "confidence": round(confidence, 2),
        "model_id": f"specialist-{key}",
        "base_model": meta.get("base_model", "distilbert-base-uncased"),
        "eval_accuracy": meta.get("eval_accuracy"),
        "class_probabilities": {
            LABELS[i]: round(float(probs[i].item()), 4) for i in range(len(LABELS))
        },
    }
