from backend.chroma_db import collection


def search_claims(
    query: str,
    n_results: int = 5,
):
    """Search ChromaDB for claims related to the query."""

    if not query or not query.strip():
        return []

    count = collection.count()

    if count == 0:
        return []

    n_results = min(
        n_results,
        count
    )

    results = collection.query(
        query_texts=[query.strip()],
        n_results=n_results,
    )

    ids = results.get("ids", [[]])[0]
    documents = results.get("documents", [[]])[0]
    metadatas = results.get("metadatas", [[]])[0]
    distances = results.get("distances", [[]])[0]

    formatted_results = []

    for i, claim_id in enumerate(ids):

        formatted_results.append(
            {
                "id": claim_id,

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

                "distance": (
                    distances[i]
                    if i < len(distances)
                    else None
                ),
            }
        )

    return formatted_results


if __name__ == "__main__":

    query = "The Earth revolves around the Sun."

    results = search_claims(query)

    print("\nSearch Results:")

    for result in results:
        print(result)