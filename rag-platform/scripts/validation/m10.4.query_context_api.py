import json

import requests


BASE_URL = "http://127.0.0.1:8000"

QUERIES = [
    "What is the company's policy for working from home?",
    "How much maternity leave is available in Germany?",
    "Does being on a PIP remove an employee's right to annual leave?",
]


def run_query(query: str) -> None:
    print("=" * 80)
    print(f"QUERY: {query}")
    print("=" * 80)

    response = requests.post(
        f"{BASE_URL}/query",
        json={
            "query": query,
            "top_k": 5,
        },
        timeout=120,
    )

    print(f"HTTP status: {response.status_code}")

    response.raise_for_status()

    body = response.json()

    print(f"Results: {body['result_count']}")

    context = body["context"]

    print(f"Context chunks: {context['chunk_count']}")
    print(f"Context tokens: {context['token_count']}")

    print("\nContext:")
    print(context["text"])

    print("\nContext provenance:")
    for chunk in context["chunks"]:
        print(
            f"  rank={chunk['rank']} "
            f"score={chunk['score']:.6f} "
            f"tokens={chunk['token_count']} "
            f"document={chunk['document_id']} "
            f"chunk={chunk['chunk_id']}"
        )

    print()


def main() -> None:
    response = requests.get(
        f"{BASE_URL}/health",
        timeout=10,
    )

    response.raise_for_status()

    print(json.dumps(response.json(), indent=2))
    print()

    for query in QUERIES:
        run_query(query)


if __name__ == "__main__":
    main()