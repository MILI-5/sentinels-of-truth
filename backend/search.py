from backend.chroma_db import collection


def search_claims(query: str, n_results: int = 5):
    """
    Search ChromaDB and return clean, structured results.
    """

    results = collection.query(
        query_texts=[query],
        n_results=n_results
    )

    formatted_results = []

    ids = results.get("ids", [[]])[0]
    documents = results.get("documents", [[]])[0]
    metadatas = results.get("metadatas", [[]])[0]
    distances = results.get("distances", [[]])[0]

    for i in range(len(ids)):
        formatted_results.append(
            {
                "id": ids[i],
                "text": documents[i],
                "metadata": metadatas[i],
                "distance": distances[i]
            }
        )

    return formatted_results


if __name__ == "__main__":

    query = "What revolves around the Sun?"

    results = search_claims(query)

    print("\nSearch Results:")

    for result in results:
        print(result)