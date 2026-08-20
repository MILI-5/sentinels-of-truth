from chroma_db import add_claim
from search import search_claims


# Add test claims
add_claim(
    claim_id="test_claim_002",
    text="Water freezes at 0 degrees Celsius under standard atmospheric pressure.",
    metadata={
        "source": "test",
        "type": "claim"
    }
)

add_claim(
    claim_id="test_claim_003",
    text="The Pacific Ocean is the largest ocean on Earth.",
    metadata={
        "source": "test",
        "type": "claim"
    }
)


# Test searches
queries = [
    "At what temperature does water freeze?",
    "Which is the largest ocean?",
    "What revolves around the Sun?"
]


for query in queries:

    print("\nQuery:", query)

    results = search_claims(query, n_results=2)

    for result in results:
        print(result)