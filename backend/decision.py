from typing import Any


def decide_action(
    alpha_status: str,
    beta_status: str,
) -> dict[str, Any]:
    """Determine the final claim decision."""

    if (
        alpha_status == "EVIDENCE_FOUND"
        and beta_status == "NO_MATCH"
    ):
        return {
            "decision": "INSERT",
            "reason": (
                "Supporting evidence was found and "
                "the claim is not already present "
                "in the knowledge base."
            ),
        }

    if (
        alpha_status == "EVIDENCE_FOUND"
        and beta_status == "MATCH"
    ):
        return {
            "decision": "DISCARD",
            "reason": (
                "The claim is already verified "
                "in the knowledge base."
            ),
        }

    if beta_status == "CONTRADICTION":
        return {
            "decision": "FLAG",
            "reason": (
                "The claim conflicts with a "
                "rejected claim in the knowledge base."
            ),
        }

    if (
        alpha_status == "NO_EVIDENCE"
        and beta_status == "NO_MATCH"
    ):
        return {
            "decision": "FLAG",
            "reason": (
                "No supporting evidence or existing "
                "knowledge was found."
            ),
        }

    if alpha_status == "EVIDENCE_FOUND":
        return {
            "decision": "INSERT",
            "reason": (
                "Supporting evidence was found "
                "for the claim."
            ),
        }

    return {
        "decision": "FLAG",
        "reason": (
            "The available information is insufficient "
            "to make a reliable decision."
        ),
    }