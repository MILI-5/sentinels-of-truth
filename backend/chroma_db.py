import chromadb
from pathlib import Path


BASE_DIR = Path(__file__).resolve().parent.parent
CHROMA_PATH = BASE_DIR / "data" / "chroma"

client = chromadb.PersistentClient(
    path=str(CHROMA_PATH)
)

collection = client.get_or_create_collection(
    name="claims"
)


DEFAULT_CLAIMS = [
    {
        "id": "knowledge_earth_sun",
        "text": "The Earth revolves around the Sun.",
        "metadata": {
            "source": "Sentinels Knowledge Base",
            "type": "verified_fact"
        }
    },
    {
        "id": "knowledge_sun_star",
        "text": "The Sun is a star.",
        "metadata": {
            "source": "Sentinels Knowledge Base",
            "type": "verified_fact"
        }
    },
    {
        "id": "knowledge_moon_earth",
        "text": "The Moon revolves around the Earth.",
        "metadata": {
            "source": "Sentinels Knowledge Base",
            "type": "verified_fact"
        }
    },
    {
        "id": "knowledge_water_freezing",
        "text": "Water freezes at 0 degrees Celsius under standard atmospheric pressure.",
        "metadata": {
            "source": "Sentinels Knowledge Base",
            "type": "verified_fact"
        }
    },
    {
        "id": "knowledge_pacific_ocean",
        "text": "The Pacific Ocean is the largest ocean on Earth.",
        "metadata": {
            "source": "Sentinels Knowledge Base",
            "type": "verified_fact"
        }
    }
]


def initialize_knowledge_base():
    for claim in DEFAULT_CLAIMS:
        collection.upsert(
            ids=[claim["id"]],
            documents=[claim["text"]],
            metadatas=[claim["metadata"]]
        )


def add_claim(
    claim_id: str,
    text: str,
    metadata: dict | None = None
):
    collection.upsert(
        ids=[claim_id],
        documents=[text],
        metadatas=[metadata or {}]
    )


def get_collection_count():
    return collection.count()


initialize_knowledge_base()


if __name__ == "__main__":
    initialize_knowledge_base()

    print("ChromaDB initialized successfully.")
    print("Documents stored:", get_collection_count())