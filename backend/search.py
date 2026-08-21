from typing import Any

from backend.chroma_db import collection


def search_claims(
    query: str,
    n_results: int = 5
) -> list[dict[str, Any]]:
    """
    Search ChromaDB and return structured results.
    """

    if not query or not query.strip():
        return []

    results = collection.query(
        query_texts=[query.strip()],
        n_results=n_results
    )

    ids = results.get("ids", [[]])[0]
    documents = results.get("documents", [[]])[0]
    metadatas = results.get("metadatas", [[]])[0]
    distances = results.get("distances", [[]])[0]

    formatted_results = []

    for i in range(len(ids)):

        distance = (
            distances[i]
            if i < len(distances)
            else None
        )

        formatted_results.append(
            {
                "id": ids[i],
                "text": (
                    documents[i]
                    if i < len(documents)
                    else ""
                ),
                "metadata": (
                    metadatas[i]
                    if i < len(metadatas)
                    else {}
                ),
                "distance": distance,
            }
        )

    return formatted_results


if __name__ == "__main__":

    query = "The sun is a star"

    results = search_claims(query)

    print("\nSearch Results:")

    for result in results:
        print(result)