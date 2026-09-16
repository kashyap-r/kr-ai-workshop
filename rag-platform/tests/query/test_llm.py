from rag_platform.query.llm import LLMQueryUnderstanding
from rag_platform.query.models import QueryUnderstandingRequest


def test_llm_requires_api_key() -> None:
    client = LLMQueryUnderstanding(api_key=None)
    request = QueryUnderstandingRequest("What about Germany?")

    # Avoid depending on the developer machine environment.
    client._api_key = None

    try:
        client.understand(request)
        raise AssertionError("Expected RuntimeError")
    except RuntimeError as exc:
        assert str(exc) == "GEMINI_API_KEY is not configured."
