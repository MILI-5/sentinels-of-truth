from datetime import datetime
from typing import Any

from backend.database import insert_claim
from backend.chroma_db import add_claim


def execute_insert(
    claim_id: str,
    claim: str,
    confidence: float,
    evidence: list[dict[str, Any]],
    reasoning: str,
) -> dict[str, Any]:
    """
    Insert a verified claim into both the SQLite
    knowledge base and ChromaDB.
    """

    source = None

    if evidence:

        metadata = evidence[0].get(
            "metadata",
            {}
        )

        source = metadata.get("source")

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

    add_claim(
        claim_id=claim_id,
        text=claim,
        metadata={
            "source": source or "Sentinels of Truth",
            "type": "verified_claim",
            "verification_status": "verified",
            "confidence": str(confidence),
        }
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
    Discard a claim without inserting it
    into the knowledge base.
    """

    return {
        "action": "DISCARD",
        "status": "SUCCESS",
        "claim_id": claim_id,
        "claim": claim,
        "reason": reason,
    }