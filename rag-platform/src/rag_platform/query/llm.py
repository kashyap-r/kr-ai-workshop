import json
import os
from collections.abc import Mapping
from urllib import error, request

from rag_platform.logging import configure_logging
from rag_platform.query.models import (
    QueryUnderstandingMode,
    QueryUnderstandingRequest,
    QueryUnderstandingResult,
)

logger = configure_logging(
    logger_name=__name__,
    log_file="logs/query_understanding.log",
)


class LLMQueryUnderstanding:
    """Gemini-backed query understanding using the REST API."""

    def __init__(
        self,
        *,
        api_key: str | None = None,
        model: str | None = None,
        timeout_seconds: float = 10.0,
    ) -> None:
        self._api_key = api_key or os.getenv("GEMINI_API_KEY")
        self._model = model or os.getenv("GEMINI_MODEL", "gemini-3.5-flash")
        self._timeout_seconds = timeout_seconds

    @property
    def available(self) -> bool:
        return bool(self._api_key)

    def understand(self, request_data: QueryUnderstandingRequest) -> QueryUnderstandingResult:
        if not self._api_key:
            raise RuntimeError("GEMINI_API_KEY is not configured.")

        context_text = ""
        if request_data.context and request_data.context.conversation:
            context_text = json.dumps(request_data.context.conversation, ensure_ascii=False)

        prompt = f"""You are a query-understanding component for an HR RAG system.
Return ONLY valid JSON with these keys:
intent, entities, filters, rewritten_query, expanded_queries.
Use empty objects/lists and null when not applicable.
Do not invent facts. Preserve entities from the user query.

User query:
{request_data.query}

Conversation context, if any:
{context_text or 'None'}
"""

        url = (
            "https://generativelanguage.googleapis.com/v1beta/models/"
            f"{self._model}:generateContent?key={self._api_key}"
        )
        body = {
            "contents": [{"parts": [{"text": prompt}]}],
            "generationConfig": {"temperature": 0, "responseMimeType": "application/json"},
        }

        payload = json.dumps(body).encode("utf-8")
        http_request = request.Request(
            url,
            data=payload,
            headers={"Content-Type": "application/json"},
            method="POST",
        )

        try:
            with request.urlopen(http_request, timeout=self._timeout_seconds) as response:
                response_data = json.loads(response.read().decode("utf-8"))
        except (error.URLError, TimeoutError, json.JSONDecodeError) as exc:
            logger.exception(
                "query_understanding_llm_failed",
                extra={"model": self._model, "error_type": type(exc).__name__},
            )
            raise RuntimeError("LLM query understanding failed.") from exc

        try:
            text = response_data["candidates"][0]["content"]["parts"][0]["text"]
            parsed = json.loads(text)
        except (KeyError, IndexError, TypeError, json.JSONDecodeError) as exc:
            logger.exception(
                "query_understanding_llm_invalid_response",
                extra={"model": self._model},
            )
            raise RuntimeError("LLM returned an invalid query-understanding response.") from exc

        entities = _string_mapping(parsed.get("entities", {}))
        filters = _string_mapping(parsed.get("filters", {}))
        expanded = tuple(str(item) for item in parsed.get("expanded_queries", []))
        rewritten = parsed.get("rewritten_query")
        rewritten = str(rewritten).strip() if rewritten else None

        result = QueryUnderstandingResult(
            original_query=request_data.query,
            normalized_query=" ".join(request_data.query.strip().split()),
            rewritten_query=rewritten,
            intent=str(parsed.get("intent")) if parsed.get("intent") else None,
            entities=entities,
            filters=filters,
            expanded_queries=expanded,
            strategy=QueryUnderstandingMode.LLM,
        )

        logger.info(
            "query_understanding_llm_completed",
            extra={
                "model": self._model,
                "intent": result.intent,
                "entity_count": len(result.entities),
                "filter_count": len(result.filters),
                "expanded_query_count": len(result.expanded_queries),
            },
        )
        return result


def _string_mapping(value: object) -> dict[str, str]:
    if not isinstance(value, Mapping):
        return {}
    return {str(key): str(item) for key, item in value.items()}
