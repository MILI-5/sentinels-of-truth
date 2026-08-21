from typing import Any

from backend.database import get_all_claims


def normalize_claim(claim: str) -> str:
    """
    Normalize a claim for comparison.
    """

    return " ".join(
        claim.strip().lower().split()
    )


def investigate_knowledge_base(
    claim: str,
) -> dict[str, Any]:
    """
    Agent Beta searches the SQLite knowledge base
    and compares the incoming claim with stored claims.
    """

    all_claims = get_all_claims()

    normalized_claim = normalize_claim(claim)

    database_matches = []

    for stored_claim in all_claims:

        stored_text = stored_claim.get(
            "claim",
            ""
        )

        if normalize_claim(stored_text) == normalized_claim:

            database_matches.append(
                stored_claim
            )

    if not database_matches:

        comparison_status = "NO_MATCH"

        contradiction_info = {
            "has_contradiction": False,
            "reason": "No matching claim found."
        }

    else:

        existing_claim = database_matches[0]

        verification_status = (
            existing_claim.get(
                "verification_status"
            )
        )

        if verification_status == "verified":

            comparison_status = "MATCH"

            contradiction_info = {
                "has_contradiction": False,
                "reason": "Existing claim is verified.",
                "database_match": existing_claim
            }

        elif verification_status == "rejected":

            comparison_status = "CONTRADICTION"

            contradiction_info = {
                "has_contradiction": True,
                "reason": (
                    "Existing claim is marked as rejected."
                ),
                "database_match": existing_claim
            }

        else:

            comparison_status = "UNKNOWN"

            contradiction_info = {
                "has_contradiction": False,
                "reason": (
                    "Existing claim has an unknown "
                    "verification status."
                ),
                "database_match": existing_claim
            }

    return {
        "claim": claim,
        "database_matches": database_matches,
        "match_found": bool(database_matches),
        "comparison_status": comparison_status,
        "contradiction_info": contradiction_info,
    }


if __name__ == "__main__":

    claim = "The Moon is made entirely of cheese."

    result = investigate_knowledge_base(claim)

    print("\nAgent Beta Investigation:")

    print("Claim:", result["claim"])

    print(
        "Match Found:",
        result["match_found"]
    )

    print(
        "Comparison Status:",
        result["comparison_status"]
    )

    print(
        "Contradiction Info:",
        result["contradiction_info"]
    )

    print("\nDatabase Matches:")

    for match in result["database_matches"]:
        print(match)