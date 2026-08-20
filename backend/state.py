from typing import Any, TypedDict


class InvestigationState(TypedDict):
    """
    Shared state passed between the agents during an investigation.
    """

    # Request information
    claim_id: str
    original_claim: str

    # Alpha / research information
    parsed_claim: dict[str, Any]
    missing_information: list[str]
    search_queries_used: list[str]
    search_results: list[dict[str, Any]]
    evidence: list[dict[str, Any]]
    verification_report: dict[str, Any]
    confidence: float

    # Beta / knowledge-base information
    database_matches: list[dict[str, Any]]
    contradiction_info: dict[str, Any]
    final_decision: str | None
    decision_reasoning: str | None

    # Execution information
    investigation_history: list[dict[str, Any]]
    timestamps: dict[str, str]

    # Error information
    errors: list[dict[str, Any]]