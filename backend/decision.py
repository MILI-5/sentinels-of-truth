from typing import Any


def decide_action(
    alpha_status: str,
    beta_status: str,
) -> dict[str, Any]:
    """
    Decide whether a claim should be INSERTED,
    FLAGGED, or DISCARDED.
    """

    # Evidence exists and claim is not already known.
    if alpha_status == "EVIDENCE_FOUND" and beta_status == "NO_MATCH":
        return {
            "decision": "INSERT",
            "reason": "Evidence found and no matching claim exists in the knowledge base."
        }

    # Evidence exists and the same claim is already verified.
    if alpha_status == "EVIDENCE_FOUND" and beta_status == "MATCH":
        return {
            "decision": "DISCARD",
            "reason": "Claim is already verified in the knowledge base."
        }

    # Evidence conflicts with the knowledge base.
    if beta_status == "CONTRADICTION":
        return {
            "decision": "FLAG",
            "reason": "Claim conflicts with a rejected claim in the knowledge base."
        }

    # No evidence and no existing knowledge.
    if alpha_status == "NO_EVIDENCE" and beta_status == "NO_MATCH":
        return {
            "decision": "FLAG",
            "reason": "No supporting evidence or existing knowledge was found."
        }

    # Safe fallback.
    return {
        "decision": "FLAG",
        "reason": "Claim requires further investigation."
    }