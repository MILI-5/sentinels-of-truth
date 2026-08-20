import chromadb
from pathlib import Path


# Project root
BASE_DIR = Path(__file__).resolve().parent.parent

# ChromaDB storage location
CHROMA_PATH = BASE_DIR / "data" / "chroma"

# Create persistent ChromaDB client
client = chromadb.PersistentClient(
    path=str(CHROMA_PATH)
)

# Create collection
collection = client.get_or_create_collection(
    name="claims"
)


def add_claim(
    claim_id: str,
    text: str,
    metadata: dict | None = None
):
    """
    Add a claim to ChromaDB.
    """

    collection.add(
        ids=[claim_id],
        documents=[text],
        metadatas=[metadata or {}]
    )


def get_collection_count():
    """
    Return number of stored documents.
    """

    return collection.count()

if __name__ == "__main__":

    test_claims = [
        {
            "id": "test_claim_001",
            "text": "The Earth revolves around the Sun.",
            "metadata": {
                "source": "test",
                "type": "claim"
            }
        },
        {
            "id": "test_claim_002",
            "text": "Water freezes at 0 degrees Celsius under standard atmospheric pressure.",
            "metadata": {
                "source": "test",
                "type": "claim"
            }
        },
        {
            "id": "test_claim_003",
            "text": "The Pacific Ocean is the largest ocean on Earth.",
            "metadata": {
                "source": "test",
                "type": "claim"
            }
        }
    ]

    for claim in test_claims:
        add_claim(
            claim_id=claim["id"],
            text=claim["text"],
            metadata=claim["metadata"]
        )

    print("ChromaDB initialized successfully.")
    print("Documents stored:", get_collection_count())