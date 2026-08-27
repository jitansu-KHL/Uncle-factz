import os
import json
import concurrent.futures
from typing import Optional, List
from pathlib import Path
from dotenv import load_dotenv
from openai import OpenAI

from backend.specialist import predict_verdict

# Load .env from either backend folder or root project folder
current_dir = Path(__file__).resolve().parent
root_dir = current_dir.parent

load_dotenv(dotenv_path=current_dir / ".env")
load_dotenv(dotenv_path=root_dir / ".env")
load_dotenv()  # Fallback to default


# ==========================================
# 4 Specialized Agent Personas
# ==========================================
AGENT_PERSONAS = [
    {
        "agent_name": "Science Agent",
        "role_description": "Scientific & Empirical Evidence Specialist",
        "persona": (
            "You are a rigorous Scientific Fact-Checking Agent specializing in empirical data, "
            "natural sciences (physics, chemistry, biology, astronomy, earth sciences), and peer-reviewed research. "
            "Evaluate claims strictly against scientific laws, peer-reviewed studies, and empirical observations. "
            "If the claim is outside the realm of natural science, evaluate whether any scientific or empirical principles apply."
        )
    },
    {
        "agent_name": "Health Agent",
        "role_description": "Medical & Public Health Specialist",
        "persona": (
            "You are a Public Health & Medical Fact-Checking Agent specializing in human biology, clinical guidelines, "
            "epidemiology, pharmaceuticals, and health consensus (e.g., WHO, CDC, FDA, major medical journals). "
            "Critique claims for medical plausibility, pseudoscience, unproven cures, and public health risks."
        )
    },
    {
        "agent_name": "Politics Agent",
        "role_description": "Policy & Government Affairs Specialist",
        "persona": (
            "You are a Political & Policy Fact-Checking Agent specializing in legislation, government actions, "
            "public policy, economics, international affairs, and official institutional records. "
            "Check whether statements accurately reflect legislative records, official statistics, or political context."
        )
    },
    {
        "agent_name": "General Agent",
        "role_description": "General Logic & Misinformation Specialist",
        "persona": (
            "You are a General Logic & Misconceptions Fact-Checking Agent specializing in critical thinking, "
            "viral internet rumors, urban legends, timeline analysis, and logical consistency. "
            "Identify sensationalist fabrications, clickbait distortions, or common misconceptions."
        )
    }
]


def get_llm_client_and_model():
    """
    Detects which API key is configured and returns the appropriate OpenAI-compatible client and model.
    """
    openai_key = os.getenv("OPENAI_API_KEY", "").strip()
    groq_key = os.getenv("GROQ_API_KEY", "").strip()
    openrouter_key = os.getenv("OPENROUTER_API_KEY", "").strip()

    # If Groq is provided explicitly or pasted in OPENAI_API_KEY
    if (groq_key and not groq_key.startswith("your_")) or openai_key.startswith("gsk_"):
        active_key = groq_key if (groq_key and not groq_key.startswith("your_")) else openai_key
        return (
            OpenAI(api_key=active_key, base_url="https://api.groq.com/openai/v1"),
            "openai/gpt-oss-120b",
            "Groq (gpt-oss-120b)"
        )

    # If OpenRouter is provided
    if openrouter_key and not openrouter_key.startswith("your_"):
        return (
            OpenAI(api_key=openrouter_key, base_url="https://openrouter.ai/api/v1"),
            "meta-llama/llama-3.3-70b-instruct:free",
            "OpenRouter"
        )

    # Default to OpenAI
    if not openai_key or openai_key.startswith("your_"):
        raise ValueError(
            "No valid API key found. Please set your GROQ_API_KEY or OPENAI_API_KEY in backend/.env"
        )

    return (
        OpenAI(api_key=openai_key),
        "gpt-4o-mini",
        "OpenAI (gpt-4o-mini)"
    )


def _template_reasoning(
    agent_name: str,
    verdict: str,
    confidence: float,
    evidence_sources: Optional[List[dict]] = None,
) -> str:
    n_sources = len(evidence_sources or [])
    src_note = (
        f"Grounded in {n_sources} retrieved source(s)."
        if n_sources
        else "Limited retrieved evidence was available."
    )
    return (
        f"{agent_name} specialist model classified this claim as '{verdict}' "
        f"(confidence {confidence:.0%}). {src_note} "
        "The verdict comes from a domain-trained classifier, not a shared general LLM prompt."
    )


def _llm_reasoning_for_verdict(
    claim: str,
    agent_name: str,
    persona: str,
    verdict: str,
    evidence_sources: Optional[List[dict]],
    model: Optional[str] = None,
) -> Optional[str]:
    """Ask the LLM only to explain a verdict already produced by the specialist."""
    try:
        client, default_model, _provider = get_llm_client_and_model()
    except ValueError:
        return None

    model_to_use = model if model and not ("groq.com" in str(client.base_url) and str(model).startswith("gpt-")) else default_model
    evidence_text = ""
    if evidence_sources:
        evidence_text = "\n\n=== RETRIEVED REAL-TIME WEB EVIDENCE SOURCES ===\n"
        for i, src in enumerate(evidence_sources, 1):
            evidence_text += (
                f"Source [{i}]: {src.get('title', 'Unknown Title')}\n"
                f"URL: {src.get('url', 'N/A')}\n"
                f"Snippet: {src.get('snippet', '')}\n\n"
            )

    system_prompt = f"""{persona}

A domain-specialist classifier already assigned this claim the verdict "{verdict}".
Write a concise reasoning paragraph from your domain perspective that is consistent with that verdict.
Cite retrieved evidence when relevant. Respond as JSON: {{"reasoning": "<text>"}}
"""
    try:
        response = client.chat.completions.create(
            model=model_to_use,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": f'Claim: "{claim}"{evidence_text}'},
            ],
            response_format={"type": "json_object"},
            temperature=0.2,
        )
        parsed = json.loads(response.choices[0].message.content)
        return parsed.get("reasoning") or None
    except Exception:
        return None


def analyze_claim_single_agent(
    claim: str,
    agent_name: str = "General Fact-Checker",
    persona: str = "You are an objective fact-checking analyst. Evaluate the claim carefully.",
    evidence_sources: Optional[List[dict]] = None,
    model: Optional[str] = None
) -> dict:
    """
    Analyze a claim with this agent's own trained classifier when available.
    Falls back to a shared LLM persona if the specialist has not been trained yet.
    """
    specialist = predict_verdict(agent_name, claim, evidence_sources)
    if specialist:
        reasoning = _llm_reasoning_for_verdict(
            claim, agent_name, persona, specialist["verdict"], evidence_sources, model
        ) or _template_reasoning(
            agent_name, specialist["verdict"], specialist["confidence"], evidence_sources
        )
        return {
            "agent_name": agent_name,
            "persona": persona,
            "verdict": specialist["verdict"],
            "confidence": specialist["confidence"],
            "reasoning": reasoning,
            "model_id": specialist["model_id"],
        }

    client, default_model, provider_label = get_llm_client_and_model()
    model_to_use = model if model and not ("groq.com" in str(client.base_url) and model.startswith("gpt-")) else default_model

    # Format evidence context for prompt grounding
    evidence_text = ""
    if evidence_sources:
        evidence_text = "\n\n=== RETRIEVED REAL-TIME WEB EVIDENCE SOURCES ===\n"
        for i, src in enumerate(evidence_sources, 1):
            evidence_text += (
                f"Source [{i}]: {src.get('title', 'Unknown Title')}\n"
                f"URL: {src.get('url', 'N/A')}\n"
                f"Snippet: {src.get('snippet', '')}\n\n"
            )
        evidence_text += "Use the above evidence sources to verify or refute the claim. Cite specific findings in your reasoning."

    system_prompt = f"""{persona}

Your task is to analyze the given claim based on verifiable facts and the provided search evidence.
Allowed verdicts:
- "True" (The claim is fully accurate and supported by facts)
- "Mostly True" (The core claim is true, but may lack minor nuance)
- "False" (The claim is demonstrably false, fabricated, or thoroughly debunked)
- "Insufficient Evidence" (There is not enough verifiable information to confirm or refute)

You MUST respond with valid JSON matching this exact structure:
{{
  "verdict": "True" | "Mostly True" | "False" | "Insufficient Evidence",
  "confidence": <float between 0.0 and 1.0 representing how confident you are>,
  "reasoning": "<concise explanation of your evaluation, citing specific evidence or why it's true/false from your specialized domain perspective>"
}}
"""

    user_prompt = f"Claim to evaluate: \"{claim}\"{evidence_text}"

    response = client.chat.completions.create(
        model=model_to_use,
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt},
        ],
        response_format={"type": "json_object"},
        temperature=0.2,
    )

    content = response.choices[0].message.content
    parsed = json.loads(content)

    # Validate and normalize fields
    verdict = parsed.get("verdict", "Insufficient Evidence")
    if verdict not in ["True", "Mostly True", "False", "Insufficient Evidence"]:
        verdict = "Insufficient Evidence"

    confidence = float(parsed.get("confidence", 0.7))
    confidence = max(0.0, min(1.0, confidence))  # Clamp between 0.0 and 1.0

    reasoning = parsed.get("reasoning", "No reasoning provided.")

    return {
        "agent_name": agent_name,
        "persona": persona,
        "verdict": verdict,
        "confidence": round(confidence, 2),
        "reasoning": reasoning,
        "model_id": f"llm:{provider_label}",
    }


def run_all_agents_parallel(
    claim: str,
    evidence_sources: Optional[List[dict]] = None
) -> List[dict]:
    """
    Executes all 4 specialized fact-checking agents concurrently in parallel threads.
    Returns a list of 4 structured agent verdicts.
    """
    with concurrent.futures.ThreadPoolExecutor(max_workers=4) as executor:
        future_to_agent = {
            executor.submit(
                analyze_claim_single_agent,
                claim=claim,
                agent_name=agent_config["agent_name"],
                persona=agent_config["persona"],
                evidence_sources=evidence_sources,
            ): agent_config["agent_name"]
            for agent_config in AGENT_PERSONAS
        }

        results = []
        for future in concurrent.futures.as_completed(future_to_agent):
            try:
                res = future.result()
                results.append(res)
            except Exception as e:
                agent_name = future_to_agent[future]
                results.append({
                    "agent_name": agent_name,
                    "persona": "Specialized Domain Analyst",
                    "verdict": "Insufficient Evidence",
                    "confidence": 0.5,
                    "reasoning": f"Agent evaluation error: {str(e)}",
                    "model_id": "error",
                })

    # Keep consistent ordering: Science, Health, Politics, General
    order = ["Science Agent", "Health Agent", "Politics Agent", "General Agent"]
    results.sort(key=lambda x: order.index(x["agent_name"]) if x["agent_name"] in order else 99)
    return results
