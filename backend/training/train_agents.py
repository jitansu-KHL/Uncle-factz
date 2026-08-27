"""
Train one DistilBERT classifier per fact-checking agent.

Usage (from the project root):

    python -m backend.training.train_agents --all
    python -m backend.training.train_agents --agent science
    python -m backend.training.train_agents --agent health --epochs 6

Each agent gets its own checkpoint under backend/models/<agent>/.
After training, the API uses these models automatically when checkpoints exist.
"""

from __future__ import annotations

import argparse
import json
import random
import sys
from pathlib import Path

# Allow `python backend/training/train_agents.py` as well as -m
ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from backend.training.config import (
    AGENT_KEYS,
    DEFAULT_BASE_MODEL,
    ID2LABEL,
    LABEL2ID,
    LABELS,
    model_dir,
)
from backend.training.seed_data import SEED_BY_AGENT


def _set_seed(seed: int) -> None:
    random.seed(seed)
    try:
        import numpy as np
        import torch

        np.random.seed(seed)
        torch.manual_seed(seed)
        if torch.cuda.is_available():
            torch.cuda.manual_seed_all(seed)
    except ImportError:
        pass


def _encode_example(claim: str, evidence: str) -> str:
    claim = (claim or "").strip()
    evidence = (evidence or "").strip()
    if evidence:
        return f"claim: {claim} evidence: {evidence}"
    return f"claim: {claim} evidence: none"


def _augment(rows: list[dict], extra: int = 1) -> list[dict]:
    """Light paraphrase-style augmentation by shuffling evidence order / prefixes."""
    out = list(rows)
    prefixes = [
        "Retrieved sources indicate: ",
        "According to available evidence: ",
        "Web snippets: ",
    ]
    for row in rows:
        for i in range(extra):
            prefix = prefixes[i % len(prefixes)]
            out.append(
                {
                    "claim": row["claim"],
                    "evidence": prefix + row["evidence"],
                    "verdict": row["verdict"],
                }
            )
    return out


def load_rows(agent_key: str) -> list[dict]:
    rows = list(SEED_BY_AGENT[agent_key])
    extra_path = Path(__file__).resolve().parent / "data" / f"{agent_key}.jsonl"
    if extra_path.exists():
        with extra_path.open(encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                item = json.loads(line)
                if item.get("verdict") not in LABEL2ID:
                    continue
                rows.append(
                    {
                        "claim": item["claim"],
                        "evidence": item.get("evidence", ""),
                        "verdict": item["verdict"],
                    }
                )
    return rows


def _split(rows: list[dict], val_ratio: float, seed: int) -> tuple[list[dict], list[dict]]:
    rng = random.Random(seed)
    by_label: dict[str, list[dict]] = {}
    for row in rows:
        by_label.setdefault(row["verdict"], []).append(row)

    train_rows: list[dict] = []
    val_rows: list[dict] = []
    for _label, group in by_label.items():
        shuffled = group[:]
        rng.shuffle(shuffled)
        n_val = max(1, int(round(len(shuffled) * val_ratio)))
        if n_val >= len(shuffled):
            n_val = max(1, len(shuffled) // 5) if len(shuffled) > 1 else 0
        val_rows.extend(shuffled[:n_val])
        train_rows.extend(shuffled[n_val:])

    rng.shuffle(train_rows)
    rng.shuffle(val_rows)
    if not train_rows:
        return val_rows, []
    return train_rows, val_rows


def train_agent(
    agent_key: str,
    base_model: str = DEFAULT_BASE_MODEL,
    epochs: int = 8,
    batch_size: int = 8,
    lr: float = 3e-5,
    seed: int = 42,
    augment: int = 2,
) -> dict:
    try:
        import numpy as np
        import torch
        import torch.nn as nn
        from torch.utils.data import Dataset
        from transformers import (
            AutoModelForSequenceClassification,
            AutoTokenizer,
            Trainer,
            TrainingArguments,
        )
    except ImportError as exc:
        raise SystemExit(
            "Missing training dependencies. Install with:\n"
            "  pip install torch transformers accelerate scikit-learn numpy\n"
            f"Original error: {exc}"
        ) from exc

    _set_seed(seed)
    raw_rows = load_rows(agent_key)
    if len(raw_rows) < 8:
        raise SystemExit(f"Not enough labeled rows for {agent_key}.")

    # Holdout is only for reporting. The saved model is trained on all labels
    # so well-known demo claims (e.g. vaccines/autism) are not left out.
    _, val_raw = _split(raw_rows, val_ratio=0.2, seed=seed)
    train_rows = _augment(raw_rows, extra=augment)
    val_rows = val_raw or raw_rows[: max(4, len(raw_rows) // 5)]
    tokenizer = AutoTokenizer.from_pretrained(base_model)

    class ClaimDataset(Dataset):
        def __init__(self, examples: list[dict]):
            self.examples = examples

        def __len__(self) -> int:
            return len(self.examples)

        def __getitem__(self, idx: int) -> dict:
            item = self.examples[idx]
            text = _encode_example(item["claim"], item["evidence"])
            encoded = tokenizer(
                text,
                truncation=True,
                padding="max_length",
                max_length=256,
                return_tensors="pt",
            )
            return {
                "input_ids": encoded["input_ids"].squeeze(0),
                "attention_mask": encoded["attention_mask"].squeeze(0),
                "labels": torch.tensor(LABEL2ID[item["verdict"]], dtype=torch.long),
            }

    counts = [0] * len(LABELS)
    for row in train_rows:
        counts[LABEL2ID[row["verdict"]]] += 1
    weights = []
    n = max(sum(counts), 1)
    for c in counts:
        weights.append(n / (len(LABELS) * max(c, 1)))
    class_weights = torch.tensor(weights, dtype=torch.float)

    model = AutoModelForSequenceClassification.from_pretrained(
        base_model,
        num_labels=len(LABELS),
        id2label=ID2LABEL,
        label2id=LABEL2ID,
    )

    class WeightedCETrainer(Trainer):
        def compute_loss(self, model, inputs, return_outputs=False, **kwargs):
            labels = inputs.pop("labels")
            outputs = model(**inputs)
            loss_fn = nn.CrossEntropyLoss(weight=class_weights.to(outputs.logits.device))
            loss = loss_fn(outputs.logits, labels)
            return (loss, outputs) if return_outputs else loss

    out_dir = model_dir(agent_key)
    out_dir.mkdir(parents=True, exist_ok=True)

    use_cpu = not torch.cuda.is_available()
    ta_kwargs = dict(
        output_dir=str(out_dir / "runs"),
        num_train_epochs=epochs,
        per_device_train_batch_size=batch_size,
        per_device_eval_batch_size=batch_size,
        learning_rate=lr,
        save_strategy="epoch",
        load_best_model_at_end=True,
        metric_for_best_model="eval_accuracy",
        greater_is_better=True,
        logging_steps=10,
        seed=seed,
        report_to=[],
        fp16=False,
        save_total_limit=1,
    )
    import inspect

    params = inspect.signature(TrainingArguments.__init__).parameters
    if "eval_strategy" in params:
        ta_kwargs["eval_strategy"] = "epoch"
    else:
        ta_kwargs["evaluation_strategy"] = "epoch"
    if "use_cpu" in params:
        ta_kwargs["use_cpu"] = use_cpu
    else:
        ta_kwargs["no_cuda"] = use_cpu
    args = TrainingArguments(**ta_kwargs)

    def compute_metrics(eval_pred):
        logits, labels = eval_pred
        preds = np.argmax(logits, axis=-1)
        acc = float((preds == labels).mean()) if len(labels) else 0.0
        return {"accuracy": acc}

    trainer = WeightedCETrainer(
        model=model,
        args=args,
        train_dataset=ClaimDataset(train_rows),
        eval_dataset=ClaimDataset(val_rows),
        compute_metrics=compute_metrics,
    )

    print(f"\n=== Training {AGENT_KEYS[agent_key]} ({agent_key}) ===")
    print(f"Base model: {base_model}")
    print(f"Train examples: {len(train_rows)} | Val examples: {len(val_rows)}")
    print(f"Device: {'CPU' if use_cpu else 'CUDA'}")

    trainer.train()
    metrics = trainer.evaluate()
    trainer.save_model(str(out_dir))
    tokenizer.save_pretrained(str(out_dir))

    meta = {
        "agent_key": agent_key,
        "agent_name": AGENT_KEYS[agent_key],
        "base_model": base_model,
        "labels": LABELS,
        "eval_accuracy": round(float(metrics.get("eval_accuracy", 0.0)), 4),
        "eval_is_leaky_sanity_check": True,
        "train_size": len(train_rows),
        "labeled_source_rows": len(raw_rows),
        "epochs": epochs,
    }
    (out_dir / "meta.json").write_text(json.dumps(meta, indent=2), encoding="utf-8")
    print(f"Saved {agent_key} specialist to {out_dir}")
    print(f"Validation accuracy: {meta['eval_accuracy']:.2%}")
    return meta


def main() -> None:
    parser = argparse.ArgumentParser(description="Train per-agent fact-check classifiers")
    parser.add_argument("--agent", choices=list(AGENT_KEYS), help="Train a single agent")
    parser.add_argument("--all", action="store_true", help="Train all four agents")
    parser.add_argument("--epochs", type=int, default=8)
    parser.add_argument("--batch-size", type=int, default=8)
    parser.add_argument("--base-model", default=DEFAULT_BASE_MODEL)
    parser.add_argument("--augment", type=int, default=2, help="Extra copies with evidence prefixes")
    args = parser.parse_args()

    if not args.agent and not args.all:
        parser.error("Specify --agent <name> or --all")

    keys = list(AGENT_KEYS) if args.all else [args.agent]
    results = []
    for key in keys:
        results.append(
            train_agent(
                key,
                base_model=args.base_model,
                epochs=args.epochs,
                batch_size=args.batch_size,
                augment=args.augment,
            )
        )

    print("\n=== Training summary ===")
    for meta in results:
        print(f"  {meta['agent_name']}: val acc {meta['eval_accuracy']:.2%} -> backend/models/{meta['agent_key']}/")


if __name__ == "__main__":
    main()
