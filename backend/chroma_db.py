import chromadb
from pathlib import Path


BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "data"
CHROMA_PATH = DATA_DIR / "chroma"

DATA_DIR.mkdir(parents=True, exist_ok=True)
CHROMA_PATH.mkdir(parents=True, exist_ok=True)


client = chromadb.PersistentClient(
    path=str(CHROMA_PATH)
)

collection = client.get_or_create_collection(
    name="claims"
)


DEFAULT_CLAIMS = [
    {
        "id": "knowledge_001",
        "text": "The Earth revolves around the Sun.",
        "metadata": {
            "source": "Sentinels of Truth knowledge base",
            "type": "verified_claim",
            "verification_status": "verified",
        },
    },
    {
        "id": "knowledge_002",
        "text": "Water freezes at 0 degrees Celsius under standard atmospheric pressure.",
        "metadata": {
            "source": "Sentinels of Truth knowledge base",
            "type": "verified_claim",
            "verification_status": "verified",
        },
    },
    {
        "id": "knowledge_003",
        "text": "The Pacific Ocean is the largest ocean on Earth.",
        "metadata": {
            "source": "Sentinels of Truth knowledge base",
            "type": "verified_claim",
            "verification_status": "verified",
        },
    },
]


def initialize_collection():
    """Insert default claims if they are not already stored."""

    existing = collection.get(
        ids=[claim["id"] for claim in DEFAULT_CLAIMS]
    )

    existing_ids = set(existing.get("ids", []))

    new_claims = [
        claim
        for claim in DEFAULT_CLAIMS
        if claim["id"] not in existing_ids
    ]

    if not new_claims:
        return

    collection.add(
        ids=[claim["id"] for claim in new_claims],
        documents=[claim["text"] for claim in new_claims],
        metadatas=[claim["metadata"] for claim in new_claims],
    )


def add_claim(
    claim_id: str,
    text: str,
    metadata: dict | None = None,
):
    """Add a claim to ChromaDB."""

    existing = collection.get(
        ids=[claim_id]
    )

    if existing.get("ids"):
        return

    collection.add(
        ids=[claim_id],
        documents=[text],
        metadatas=[metadata or {}],
    )


def get_collection_count():
    """Return the number of stored documents."""

    return collection.count()


initialize_collection()


if __name__ == "__main__":

    print("ChromaDB initialized successfully.")
    print(
        "Documents stored:",
        get_collection_count()
    )