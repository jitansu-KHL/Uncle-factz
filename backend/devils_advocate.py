"""
Devil's Advocate Agent Module
Challenges a specific agent's verdict by independently searching for
contradictory evidence and evaluating whether the agent's conclusion holds up.
"""

import json
from typing import List, Dict, Any, Optional
from backend.agent import get_llm_client_and_model
from backend.search import search_with_duckduckgo, search_with_wikipedia


def _build_challenge_queries(claim: str, agent_verdict: str) -> List[str]:
    """
    Generate search queries designed to find evidence that CONTRADICTS
    the agent's verdict. These are intentionally different from the
    original evidence search.
    """
    base = claim.strip().rstrip(".")
    queries = []

    if agent_verdict in ("True", "Mostly True"):
        queries.append(f'"{base}" debunked')
        queries.append(f'"{base}" false OR misleading OR myth')
        queries.append(f'"{base}" criticism OR rebuttal')
    else:
        queries.append(f'"{base}" confirmed OR verified')
        queries.append(f'"{base}" true OR evidence supports')
        queries.append(f'"{base}" fact check confirmed')

    return queries


def _search_challenge_evidence(
    claim: str,
    agent_verdict: str,
    max_results: int = 5,
) -> List[Dict[str, str]]:
    """
    Perform an independent web search specifically looking for evidence
    that contradicts the agent's verdict. Uses different search queries
    than the initial evidence retrieval.
    """
    queries = _build_challenge_queries(claim, agent_verdict)
    all_sources: List[Dict[str, str]] = []
    seen_urls = set()

    for query in queries:
        # Try DuckDuckGo first
        results = search_with_duckduckgo(query, max_results=3)
        if not results:
            results = search_with_wikipedia(query, max_results=2)

        for src in results:
            url = src.get("url", "")
            if url and url not in seen_urls:
                seen_urls.add(url)
                all_sources.append(src)

        if len(all_sources) >= max_results:
            break

    return all_sources[:max_results]


def challenge_agent_verdict(
    claim: str,
    agent_name: str,
    agent_verdict: str,
    agent_confidence: float,
    agent_reasoning: str,
    initial_sources: Optional[List[Dict[str, str]]] = None,
) -> Dict[str, Any]:
    """
    Run the Devil's Advocate against a single agent's verdict.

    1. Independently searches the web for contradictory evidence
    2. Sends the claim, agent verdict, and NEW evidence to the LLM
    3. Returns a structured challenge result
    """

    # Step 1: Independent contradictory evidence search
    challenge_sources = _search_challenge_evidence(claim, agent_verdict)

    # Format the challenge evidence for the prompt
    challenge_evidence_text = ""
    if challenge_sources:
        challenge_evidence_text = "\n\n=== INDEPENDENTLY RETRIEVED CHALLENGE EVIDENCE ===\n"
        for i, src in enumerate(challenge_sources, 1):
            challenge_evidence_text += (
                f"Source [{i}]: {src.get('title', 'Unknown')}\n"
                f"URL: {src.get('url', 'N/A')}\n"
                f"Snippet: {src.get('snippet', '')}\n\n"
            )

    # Format the original sources summary (so DA knows what was already used)
    original_sources_text = ""
    if initial_sources:
        original_sources_text = "\n\n=== ORIGINAL SOURCES ALREADY USED BY THE AGENT (do NOT re-use these) ===\n"
        for i, src in enumerate(initial_sources, 1):
            original_sources_text += f"[{i}] {src.get('title', '')} — {src.get('url', '')}\n"

    # Step 2: Build the Devil's Advocate prompt
    system_prompt = """You are a Devil's Advocate Fact-Checking Agent. Your ONLY purpose is to challenge and stress-test another AI agent's fact-checking verdict.

You must NOT simply agree with the original agent. You must actively look for reasons the verdict could be WRONG.

Your investigation checklist:
- What evidence contradicts the current verdict?
- Are the sources being relied upon trustworthy and current?
- Is any evidence outdated or no longer applicable?
- Could the claim be technically true but misleading, or vice versa?
- Is important context missing that changes the meaning?
- Are there alternative interpretations of the evidence?
- Did the original agent overlook an authoritative source?
- Could the claim's truth value have changed over time?
- Is the evidence actually about the exact same claim?

IMPORTANT RULES:
- Use the INDEPENDENTLY RETRIEVED CHALLENGE EVIDENCE to form your analysis
- Do NOT simply repeat what the original agent said
- Do NOT just say "Are you sure?" — provide specific counter-arguments
- Be honest: if you genuinely cannot find credible contradictory evidence, say so
- Never claim mathematical proof of truth or falsehood

Use language such as:
- "The evidence suggests..."
- "Contradicted by available evidence"
- "Supported by available evidence"
- "Insufficient evidence to challenge"

You MUST respond with valid JSON matching this exact structure:
{
  "challenge_status": "NO_SIGNIFICANT_CHALLENGE" | "WEAK_CHALLENGE" | "STRONG_CHALLENGE" | "VERDICT_INVALIDATED",
  "challenge_confidence": <float 0.0-1.0, how confident you are in your challenge>,
  "contradicting_evidence": ["<finding 1>", "<finding 2>"],
  "supporting_original": ["<finding that actually supports the original verdict>"],
  "explanation": "<clear explanation of why the original verdict may or may not be wrong>",
  "suggested_verdict": "True" | "Mostly True" | "False" | "Insufficient Evidence",
  "suggested_confidence": <float 0.0-1.0>
}"""

    user_prompt = f"""CLAIM: "{claim}"

AGENT BEING CHALLENGED: {agent_name}
AGENT'S VERDICT: {agent_verdict} (Confidence: {agent_confidence:.0%})
AGENT'S REASONING: {agent_reasoning}
{original_sources_text}{challenge_evidence_text}

Based on the independently retrieved challenge evidence above, critically evaluate whether {agent_name}'s verdict of "{agent_verdict}" holds up. Actively try to find flaws in their reasoning."""

    # Step 3: Call the LLM
    try:
        client, model, provider_label = get_llm_client_and_model()

        response = client.chat.completions.create(
            model=model,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt},
            ],
            response_format={"type": "json_object"},
            temperature=0.3,
        )

        content = response.choices[0].message.content
        parsed = json.loads(content)

        # Validate and normalize
        valid_statuses = [
            "NO_SIGNIFICANT_CHALLENGE",
            "WEAK_CHALLENGE",
            "STRONG_CHALLENGE",
            "VERDICT_INVALIDATED",
        ]
        challenge_status = parsed.get("challenge_status", "NO_SIGNIFICANT_CHALLENGE")
        if challenge_status not in valid_statuses:
            challenge_status = "NO_SIGNIFICANT_CHALLENGE"

        challenge_confidence = float(parsed.get("challenge_confidence", 0.5))
        challenge_confidence = max(0.0, min(1.0, challenge_confidence))

        valid_verdicts = ["True", "Mostly True", "False", "Insufficient Evidence"]
        suggested_verdict = parsed.get("suggested_verdict", agent_verdict)
        if suggested_verdict not in valid_verdicts:
            suggested_verdict = agent_verdict

        suggested_confidence = float(parsed.get("suggested_confidence", agent_confidence))
        suggested_confidence = max(0.0, min(1.0, suggested_confidence))

        contradicting = parsed.get("contradicting_evidence", [])
        if not isinstance(contradicting, list):
            contradicting = [str(contradicting)]

        supporting = parsed.get("supporting_original", [])
        if not isinstance(supporting, list):
            supporting = [str(supporting)]

        return {
            "agent_challenged": agent_name,
            "original_verdict": agent_verdict,
            "original_confidence": agent_confidence,
            "challenge_status": challenge_status,
            "challenge_confidence": round(challenge_confidence, 2),
            "contradicting_evidence": contradicting,
            "supporting_original": supporting,
            "explanation": parsed.get("explanation", "No explanation provided."),
            "suggested_verdict": suggested_verdict,
            "suggested_confidence": round(suggested_confidence, 2),
            "challenge_sources": challenge_sources,
            "sources_analyzed": len(challenge_sources),
            "contradictory_sources_found": len(contradicting),
        }

    except Exception as e:
        return {
            "agent_challenged": agent_name,
            "original_verdict": agent_verdict,
            "original_confidence": agent_confidence,
            "challenge_status": "NO_SIGNIFICANT_CHALLENGE",
            "challenge_confidence": 0.0,
            "contradicting_evidence": [],
            "supporting_original": [],
            "explanation": f"Devil's Advocate encountered an error: {str(e)}",
            "suggested_verdict": agent_verdict,
            "suggested_confidence": agent_confidence,
            "challenge_sources": [],
            "sources_analyzed": 0,
            "contradictory_sources_found": 0,
        }
