from typing import List, Dict, Any


def calculate_consensus(agents: List[Dict[str, Any]]) -> Dict[str, Any]:
    """
    Computes a weighted consensus from multiple AI agent verdicts.

    Consensus Rules:
    1. Confidence Weighting: Each agent's vote is multiplied by its confidence score (0.0 - 1.0).
    2. Contested Detection: If top conflicting verdicts (e.g. True vs False) are tied or separated
       by less than a 0.25 weighted difference, the claim is honestly marked as 'Contested'.
    3. Consensus Summary: Generates a clear, human-readable breakdown of how consensus was reached.
    """
    if not agents:
        return {
            "final_verdict": "Insufficient Evidence",
            "overall_confidence": 0.0,
            "is_contested": False,
            "consensus_summary": "No agents evaluated this claim.",
            "vote_breakdown": {},
        }

    weighted_scores: Dict[str, float] = {}
    vote_counts: Dict[str, int] = {}
    agent_grouping: Dict[str, List[str]] = {}

    total_possible_weight = 0.0

    for a in agents:
        verdict = a.get("verdict", "Insufficient Evidence")
        confidence = float(a.get("confidence", 0.5))
        agent_name = a.get("agent_name", "Agent")

        weighted_scores[verdict] = round(weighted_scores.get(verdict, 0.0) + confidence, 3)
        vote_counts[verdict] = vote_counts.get(verdict, 0) + 1
        agent_grouping.setdefault(verdict, []).append(agent_name)
        total_possible_weight += confidence

    # Sort verdicts by weighted score descending
    sorted_verdicts = sorted(weighted_scores.items(), key=lambda x: x[1], reverse=True)
    top_verdict, top_weight = sorted_verdicts[0]

    # Check for Contested state (e.g., 2 agents True vs 2 agents False with similar high confidence)
    is_contested = False
    if len(sorted_verdicts) > 1:
        second_verdict, second_weight = sorted_verdicts[1]
        
        # Define conflicting pairs (True vs False, Mostly True vs False)
        is_conflicting_pair = (
            ("True" in top_verdict and "False" in second_verdict)
            or ("False" in top_verdict and "True" in second_verdict)
            or ("Mostly True" in top_verdict and "False" in second_verdict)
            or ("False" in top_verdict and "Mostly True" in second_verdict)
        )

        weight_difference = top_weight - second_weight
        if is_conflicting_pair and (weight_difference < 0.35 and vote_counts[top_verdict] <= 2):
            is_contested = True

    if is_contested:
        final_verdict = "Contested"
        overall_confidence = round(top_weight / max(total_possible_weight, 0.01), 2)
        summary = (
            f"Contested Verdict: The network is divided. "
            f"{vote_counts.get(sorted_verdicts[0][0])} agent(s) voted '{sorted_verdicts[0][0]}' "
            f"(weight: {sorted_verdicts[0][1]}), while "
            f"{vote_counts.get(sorted_verdicts[1][0])} agent(s) voted '{sorted_verdicts[1][0]}' "
            f"(weight: {sorted_verdicts[1][1]}). Further verification is recommended."
        )
    else:
        final_verdict = top_verdict
        # Normalized overall confidence = (winning score / total weight) * avg winning confidence
        winning_agents_confs = [
            a.get("confidence", 0.5) for a in agents if a.get("verdict") == top_verdict
        ]
        avg_winner_conf = sum(winning_agents_confs) / len(winning_agents_confs)
        weight_share = top_weight / max(total_possible_weight, 0.01)
        
        # Penalize confidence slightly if there was dissent
        overall_confidence = round(avg_winner_conf * (0.7 + 0.3 * weight_share), 2)
        overall_confidence = min(1.0, max(0.1, overall_confidence))

        supporting_agents = ", ".join(agent_grouping.get(top_verdict, []))
        summary = (
            f"Consensus Reached: {vote_counts[top_verdict]} of {len(agents)} agents voted '{top_verdict}' "
            f"({supporting_agents}) with a total weighted score of {top_weight:.2f}/{total_possible_weight:.2f}."
        )

    return {
        "final_verdict": final_verdict,
        "overall_confidence": overall_confidence,
        "is_contested": is_contested,
        "consensus_summary": summary,
        "vote_breakdown": {
            k: {"count": vote_counts[k], "weighted_score": weighted_scores[k]}
            for k in weighted_scores
        },
    }
