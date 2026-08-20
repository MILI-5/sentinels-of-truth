from typing import Any

from backend.database import get_all_claims


def investigate_knowledge_base(
    claim: str,
) -> dict[str, Any]:
    """
    Agent Beta searches the SQLite knowledge base
    and compares the incoming claim with stored claims.
    """

    all_claims = get_all_claims()

    database_matches = []

    for stored_claim in all_claims:

        if stored_claim["claim"].strip().lower() == claim.strip().lower():
            database_matches.append(stored_claim)

    if not database_matches:

        comparison_status = "NO_MATCH"

        contradiction_info = {
            "has_contradiction": False,
            "reason": "No matching claim found."
        }

    else:

        verification_status = database_matches[0]["verification_status"]

        if verification_status == "verified":

            comparison_status = "MATCH"

            contradiction_info = {
                "has_contradiction": False,
                "reason": "Existing claim is verified.",
                "database_match": database_matches[0]
            }

        elif verification_status == "rejected":

            comparison_status = "CONTRADICTION"

            contradiction_info = {
                "has_contradiction": True,
                "reason": "Existing claim is marked as rejected.",
                "database_match": database_matches[0]
            }

        else:

            comparison_status = "UNKNOWN"

            contradiction_info = {
                "has_contradiction": False,
                "reason": "Existing claim has an unknown verification status.",
                "database_match": database_matches[0]
            }

    return {
        "claim": claim,
        "database_matches": database_matches,
        "match_found": len(database_matches) > 0,
        "comparison_status": comparison_status,
        "contradiction_info": contradiction_info,
    }

if __name__ == "__main__":

    claim = "The Moon is made entirely of cheese."

    result = investigate_knowledge_base(claim)

    print("\nAgent Beta Investigation:")
    print("Claim:", result["claim"])
    print("Match Found:", result["match_found"])
    print("Comparison Status:", result["comparison_status"])
    print("Contradiction Info:", result["contradiction_info"])

    print("Database Matches:")

    for match in result["database_matches"]:
        print(match)