from backend.search import search_claims


def investigate_claim(
    claim: str,
    n_results: int = 5,
    distance_threshold: float = 1.0
):
    search_results = search_claims(
        query=claim,
        n_results=n_results
    )

    evidence = [
        result
        for result in search_results
        if (
            result.get("distance") is not None
            and result["distance"] <= distance_threshold
        )
    ]

    best_evidence = evidence[0] if evidence else None

    status = (
        "EVIDENCE_FOUND"
        if evidence
        else "NO_EVIDENCE"
    )

    return {
        "claim": claim,
        "evidence": evidence,
        "evidence_count": len(evidence),
        "has_evidence": bool(evidence),
        "best_evidence": best_evidence,
        "status": status
    }


if __name__ == "__main__":

    claim = "The Earth revolves around the Sun."

    result = investigate_claim(claim)

    print("\nAgent Alpha Investigation:")
    print("Claim:", result["claim"])
    print("Status:", result["status"])
    print("Evidence Count:", result["evidence_count"])
    print("Has Evidence:", result["has_evidence"])

    print("\nBest Evidence:")
    print(result["best_evidence"])

    print("\nRelevant Evidence:")

    for item in result["evidence"]:
        print(item)