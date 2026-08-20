from datetime import datetime
from typing import Any

from backend.database import insert_claim


def execute_insert(
    claim_id: str,
    claim: str,
    confidence: float,
    evidence: list[dict[str, Any]],
    reasoning: str,
) -> dict[str, Any]:
    """
    Insert a verified claim into the SQLite knowledge base.
    """

    source = None

    if evidence:
        source = evidence[0].get("metadata", {}).get("source")

    created_at = datetime.now().isoformat()

    insert_claim(
        claim_id=claim_id,
        claim=claim,
        verification_status="verified",
        confidence=confidence,
        source=source,
        reasoning=reasoning,
        created_at=created_at,
    )

    return {
        "action": "INSERT",
        "status": "SUCCESS",
        "claim_id": claim_id,
    }

def execute_flag(
    claim_id: str,
    claim: str,
    reason: str,
) -> dict[str, Any]:
    """
    Flag a claim for human review.

    FLAG does not insert or modify the knowledge base.
    """

    return {
        "action": "FLAG",
        "status": "SUCCESS",
        "claim_id": claim_id,
        "claim": claim,
        "reason": reason,
    }

def execute_discard(
    claim_id: str,
    claim: str,
    reason: str,
) -> dict[str, Any]:
    """
    Discard a claim without inserting it into the knowledge base.
    """

    return {
        "action": "DISCARD",
        "status": "SUCCESS",
        "claim_id": claim_id,
        "claim": claim,
        "reason": reason,
    }