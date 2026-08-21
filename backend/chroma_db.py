import chromadb
from pathlib import Path


BASE_DIR = Path(__file__).resolve().parent.parent
CHROMA_PATH = BASE_DIR / "data" / "chroma"

CHROMA_PATH.mkdir(parents=True, exist_ok=True)


client = chromadb.PersistentClient(
    path=str(CHROMA_PATH)
)


collection = client.get_or_create_collection(
    name="claims"
)


def add_claim(
    claim_id: str,
    text: str,
    metadata: dict | None = None
):
    """
    Add or update a claim in ChromaDB.
    """

    collection.upsert(
        ids=[claim_id],
        documents=[text],
        metadatas=[metadata or {}]
    )


def get_collection_count() -> int:
    """
    Return the number of stored documents.
    """

    return collection.count()


def seed_demo_claims():
    """
    Add a small set of factual claims for testing.
    Existing IDs are updated instead of duplicated.
    """

    test_claims = [
        {
            "id": "fact_001",
            "text": "The Earth revolves around the Sun.",
            "metadata": {
                "source": "NASA",
                "type": "scientific_fact"
            }
        },
        {
            "id": "fact_002",
            "text": "The Sun is a star at the center of the Solar System.",
            "metadata": {
                "source": "NASA",
                "type": "scientific_fact"
            }
        },
        {
            "id": "fact_003",
            "text": "The Moon orbits the Earth.",
            "metadata": {
                "source": "NASA",
                "type": "scientific_fact"
            }
        },
        {
            "id": "fact_004",
            "text": "Water freezes at 0 degrees Celsius under standard atmospheric pressure.",
            "metadata": {
                "source": "Scientific Reference",
                "type": "scientific_fact"
            }
        },
        {
            "id": "fact_005",
            "text": "The Pacific Ocean is the largest ocean on Earth.",
            "metadata": {
                "source": "NOAA",
                "type": "geographical_fact"
            }
        },
        {
            "id": "fact_006",
            "text": "The Earth is the third planet from the Sun.",
            "metadata": {
                "source": "NASA",
                "type": "scientific_fact"
            }
        },
        {
            "id": "fact_007",
            "text": "The Sun is composed primarily of hydrogen and helium.",
            "metadata": {
                "source": "NASA",
                "type": "scientific_fact"
            }
        },
    ]

    for claim in test_claims:
        add_claim(
            claim_id=claim["id"],
            text=claim["text"],
            metadata=claim["metadata"]
        )

    return get_collection_count()


if __name__ == "__main__":

    count = seed_demo_claims()

    print("ChromaDB initialized successfully.")
    print("Documents stored:", count)