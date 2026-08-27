import sqlite3
import json
from pathlib import Path
from typing import List, Dict, Any, Optional
from datetime import datetime

DB_PATH = Path(__file__).resolve().parent / "factchecks.db"


def init_db():
    """Initializes the SQLite database table for fact check history."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS fact_checks (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            claim TEXT NOT NULL,
            final_verdict TEXT NOT NULL,
            overall_confidence REAL NOT NULL,
            consensus_summary TEXT NOT NULL,
            is_contested BOOLEAN NOT NULL,
            agents_json TEXT NOT NULL,
            sources_json TEXT NOT NULL,
            blockchain_tx TEXT,
            claim_hash TEXT,
            timestamp TEXT NOT NULL
        )
    """)
    conn.commit()
    conn.close()


def save_fact_check(
    claim: str,
    final_verdict: str,
    overall_confidence: float,
    consensus_summary: str,
    is_contested: bool,
    agents: List[Dict[str, Any]],
    sources: List[Dict[str, Any]],
    blockchain_tx: Optional[str] = None,
    claim_hash: Optional[str] = None,
    timestamp: Optional[str] = None,
):
    """Stores a fact-check record into SQLite."""
    init_db()
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    if not timestamp:
        timestamp = datetime.utcnow().isoformat() + "Z"

    cursor.execute("""
        INSERT INTO fact_checks (
            claim, final_verdict, overall_confidence, consensus_summary,
            is_contested, agents_json, sources_json, blockchain_tx, claim_hash, timestamp
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        claim,
        final_verdict,
        overall_confidence,
        consensus_summary,
        1 if is_contested else 0,
        json.dumps(agents),
        json.dumps(sources),
        blockchain_tx,
        claim_hash,
        timestamp,
    ))
    conn.commit()
    conn.close()


def get_recent_fact_checks(limit: int = 10) -> List[Dict[str, Any]]:
    """Fetches recent fact-check history from SQLite."""
    init_db()
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    cursor.execute("""
        SELECT id, claim, final_verdict, overall_confidence, consensus_summary,
               is_contested, agents_json, sources_json, blockchain_tx, claim_hash, timestamp
        FROM fact_checks
        ORDER BY id DESC
        LIMIT ?
    """, (limit,))
    
    rows = cursor.fetchall()
    results = []
    for r in rows:
        results.append({
            "id": r["id"],
            "claim": r["claim"],
            "final_verdict": r["final_verdict"],
            "overall_confidence": r["overall_confidence"],
            "consensus_summary": r["consensus_summary"],
            "is_contested": bool(r["is_contested"]),
            "agents": json.loads(r["agents_json"]),
            "sources": json.loads(r["sources_json"]),
            "blockchain_tx": r["blockchain_tx"],
            "claim_hash": r["claim_hash"],
            "timestamp": r["timestamp"],
        })
    conn.close()
    return results
