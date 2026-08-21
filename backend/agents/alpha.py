from typing import Any

from backend.search import search_claims


def investigate_claim(
    claim: str,
    n_results: int = 5,
    distance_threshold: float = 1.0
) -> dict[str, Any]:
    """
    Agent Alpha searches the ChromaDB knowledge base
    for evidence related to the incoming claim.
    """

    search_results = search_claims(
        query=claim,
        n_results=n_results
    )

    evidence = []

    for result in search_results:

        distance = result.get("distance")

        if distance is not None and distance <= distance_threshold:
            evidence.append(result)

    best_evidence = (
        evidence[0]
        if evidence
        else None
    )

    if evidence:
        status = "EVIDENCE_FOUND"
    else:
        status = "NO_EVIDENCE"

    return {
        "claim": claim,

        "search_queries": [
            claim
        ],

        "search_results": search_results,

        "evidence": evidence,

        "evidence_count": len(evidence),

        "has_evidence": bool(evidence),

        "best_evidence": best_evidence,

        "status": status,
    }


if __name__ == "__main__":

    claim = "The sun is a star"

    result = investigate_claim(claim)

    print("\nAgent Alpha Investigation:")

    print("Claim:", result["claim"])

    print("Status:", result["status"])

    print(
        "Evidence Count:",
        result["evidence_count"]
    )

    print(
        "Has Evidence:",
        result["has_evidence"]
    )

    print(
        "\nSearch Queries:"
    )

    for query in result["search_queries"]:
        print(query)

    print("\nSearch Results:")

    for item in result["search_results"]:
        print(item)

    print("\nBest Evidence:")

    print(result["best_evidence"])

    print("\nRelevant Evidence:")

    for item in result["evidence"]:
        print(item)