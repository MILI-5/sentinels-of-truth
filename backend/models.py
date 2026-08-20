from typing import Any

from pydantic import BaseModel, Field


class InvestigationRequest(BaseModel):
    claim: str


class InvestigationResponse(BaseModel):

    claim_id: str

    claim: str

    decision: str | None = None

    confidence: float = 0.0

    reasoning: str | None = None

    search_queries: list[str] = Field(
        default_factory=list
    )

    search_results: list[Any] = Field(
        default_factory=list
    )

    evidence: list[Any] = Field(
        default_factory=list
    )

    investigation_history: list[Any] = Field(
        default_factory=list
    )

    verification_report: dict[str, Any] = Field(
        default_factory=dict
    )