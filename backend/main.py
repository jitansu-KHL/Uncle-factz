from datetime import datetime
from typing import List, Optional
from pathlib import Path
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from dotenv import load_dotenv

# Load .env from backend/ and root directories
current_dir = Path(__file__).resolve().parent
root_dir = current_dir.parent
load_dotenv(dotenv_path=current_dir / ".env")
load_dotenv(dotenv_path=root_dir / ".env")
load_dotenv()

from backend.agent import run_all_agents_parallel
from backend.search import search_evidence
from backend.consensus import calculate_consensus
from backend.blockchain import record_verdict_onchain
from backend.database import save_fact_check, get_recent_fact_checks, init_db
from backend.devils_advocate import challenge_agent_verdict
from backend.specialist import list_ready_specialists, specialist_available
from backend.training.config import AGENT_KEYS

# Initialize database on startup
init_db()

app = FastAPI(
    title="Decentralized Fact-Checking Network API",
    description="Multi-Agent Consensus Fact-Checking Network with Tamper-Evident Blockchain Storage",
    version="1.0.0",
)

# Enable CORS so frontend (React/Vite) can communicate with this API
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ==========================================
# Data Models (Schemas)
# ==========================================
class ClaimRequest(BaseModel):
    claim: str = Field(
        ...,
        description="The statement or news headline to fact-check",
        example="Vaccines cause autism.",
    )


class AgentVerdict(BaseModel):
    agent_name: str = Field(..., description="Name of the agent")
    persona: str = Field(..., description="Domain specialization of the agent")
    verdict: str = Field(
        ...,
        description="Verdict: True | Mostly True | False | Insufficient Evidence",
    )
    confidence: float = Field(
        ..., ge=0.0, le=1.0, description="Confidence score between 0.0 and 1.0"
    )
    reasoning: str = Field(..., description="Explanation from this agent's perspective")
    model_id: Optional[str] = Field(
        None, description="specialist-<domain> if a trained classifier was used"
    )


class SourceEvidence(BaseModel):
    title: str
    url: str
    snippet: str


class FactCheckResponse(BaseModel):
    claim: str
    final_verdict: str = Field(
        ...,
        description="Final consensus verdict: True | Mostly True | False | Insufficient Evidence | Contested",
    )
    overall_confidence: float = Field(
        ..., ge=0.0, le=1.0, description="Aggregated confidence score"
    )
    consensus_summary: str
    is_contested: bool
    agents: List[AgentVerdict]
    sources: List[SourceEvidence]
    blockchain_tx: Optional[str] = Field(
        None, description="Transaction hash anchoring consensus proof on blockchain"
    )
    claim_hash: Optional[str] = Field(
        None, description="Cryptographic Keccak-256 hash of the claim"
    )
    timestamp: str


from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles

STATIC_DIR = Path(__file__).resolve().parent / "static"
if STATIC_DIR.exists():
    app.mount("/static", StaticFiles(directory=STATIC_DIR), name="static")

# ==========================================
# Routes
# ==========================================
@app.get("/")
def read_root():
    index_file = STATIC_DIR / "index.html"
    if index_file.exists():
        return FileResponse(index_file)
    return {
        "status": "online",
        "message": "Decentralized Fact-Checking Network API is running",
        "docs_url": "/docs",
    }


@app.get("/health")
def health_check():
    return {"status": "healthy", "timestamp": datetime.utcnow().isoformat()}


@app.get("/api/specialists")
def specialists_status():
    """Shows which agents have trained local models vs LLM-prompt fallback."""
    return {
        "agents": [
            {
                "agent_key": key,
                "agent_name": name,
                "trained": specialist_available(name),
            }
            for key, name in AGENT_KEYS.items()
        ],
        "ready": list_ready_specialists(),
    }


@app.get("/api/history")
def get_history(limit: int = 10):
    """Returns recently evaluated fact-checked claims and their on-chain proofs."""
    return get_recent_fact_checks(limit=limit)


@app.post("/api/factcheck", response_model=FactCheckResponse)
def fact_check_claim(request: ClaimRequest):
    """
    Complete Step 6 Workflow:
    1. Web Search Retrieval (Tavily/DDG/Wikipedia)
    2. 4 Parallel Specialized AI Agents (Science, Health, Politics, General)
    3. Confidence-Weighted Consensus Engine
    4. Tamper-Evident Blockchain Proof Anchoring (Keccak256 + Smart Contract)
    5. Persistent Database Storage (SQLite)
    """
    claim_text = request.claim.strip()
    if not claim_text:
        raise HTTPException(status_code=400, detail="Claim cannot be empty.")

    try:
        # 1. Retrieve real-time evidence from the web
        raw_sources = search_evidence(claim_text, max_results=5)
        source_objects = [SourceEvidence(**src) for src in raw_sources]

        # 2. Call all 4 specialized agents in parallel
        agent_results = run_all_agents_parallel(
            claim=claim_text,
            evidence_sources=raw_sources
        )
        agent_verdicts = [AgentVerdict(**res) for res in agent_results]

        # 3. Compute confidence-weighted consensus
        consensus_data = calculate_consensus(agent_results)

        # 4. Anchor on-chain proof
        blockchain_record = record_verdict_onchain(
            claim_text=claim_text,
            final_verdict=consensus_data["final_verdict"],
            overall_confidence=consensus_data["overall_confidence"],
            sources=raw_sources
        )

        now_iso = datetime.utcnow().isoformat() + "Z"

        # 5. Save to SQLite history
        save_fact_check(
            claim=claim_text,
            final_verdict=consensus_data["final_verdict"],
            overall_confidence=consensus_data["overall_confidence"],
            consensus_summary=consensus_data["consensus_summary"],
            is_contested=consensus_data["is_contested"],
            agents=agent_results,
            sources=raw_sources,
            blockchain_tx=blockchain_record["tx_hash"],
            claim_hash=blockchain_record["claim_hash"],
            timestamp=now_iso,
        )

        return FactCheckResponse(
            claim=claim_text,
            final_verdict=consensus_data["final_verdict"],
            overall_confidence=consensus_data["overall_confidence"],
            consensus_summary=consensus_data["consensus_summary"],
            is_contested=consensus_data["is_contested"],
            agents=agent_verdicts,
            sources=source_objects,
            blockchain_tx=blockchain_record["tx_hash"],
            claim_hash=blockchain_record["claim_hash"],
            timestamp=now_iso,
        )

    except ValueError as e:
        # Missing API key or configuration error
        raise HTTPException(status_code=500, detail=str(e))
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Fact-Check Error: {str(e)}"
        )


# ==========================================
# Devil's Advocate — Challenge a single agent
# ==========================================
class ChallengeRequest(BaseModel):
    claim: str = Field(..., description="The original claim that was fact-checked")
    agent_name: str = Field(..., description="Name of the agent to challenge")
    agent_verdict: str = Field(..., description="The agent's verdict to challenge")
    agent_confidence: float = Field(..., description="The agent's confidence score")
    agent_reasoning: str = Field(..., description="The agent's reasoning to challenge")


@app.post("/api/challenge-agent")
def challenge_agent(request: ChallengeRequest):
    """
    Devil's Advocate endpoint: independently challenges a specific agent's verdict
    by searching for contradictory evidence and evaluating whether the verdict holds.
    """
    try:
        result = challenge_agent_verdict(
            claim=request.claim,
            agent_name=request.agent_name,
            agent_verdict=request.agent_verdict,
            agent_confidence=request.agent_confidence,
            agent_reasoning=request.agent_reasoning,
        )
        return result
    except ValueError as e:
        raise HTTPException(status_code=500, detail=str(e))
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Devil's Advocate Error: {str(e)}"
        )
