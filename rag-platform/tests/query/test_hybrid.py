from typing import Any, cast

from rag_platform.query.hybrid import HybridQueryUnderstanding
from rag_platform.query.models import (
    QueryContext,
    QueryUnderstandingMode,
    QueryUnderstandingRequest,
    QueryUnderstandingResult,
)


class FakeLLM:
    def __init__(self) -> None:
        self.called = False
        self.available = True

    def understand(self, request: QueryUnderstandingRequest) -> QueryUnderstandingResult:
        self.called = True
        return QueryUnderstandingResult(
            original_query=request.query,
            normalized_query=request.query.strip(),
            rewritten_query="rewritten query",
            intent="policy_lookup",
            strategy=QueryUnderstandingMode.LLM,
        )


def test_hybrid_uses_rules_for_simple_query() -> None:
    llm = FakeLLM()
    service = HybridQueryUnderstanding(llm=cast(Any, llm))

    result = service.understand(
        QueryUnderstandingRequest("What is the WFH policy?")
    )

    assert result.strategy == QueryUnderstandingMode.RULE
    assert llm.called is False


def test_hybrid_uses_llm_for_complex_query() -> None:
    llm = FakeLLM()
    service = HybridQueryUnderstanding(llm=cast(Any, llm))

    result = service.understand(
        QueryUnderstandingRequest("Compare maternity leave in Germany and Sweden.")
    )

    assert result.strategy == QueryUnderstandingMode.LLM
    assert llm.called is True


def test_hybrid_uses_llm_for_contextual_query() -> None:
    llm = FakeLLM()
    service = HybridQueryUnderstanding(llm=cast(Any, llm))

    result = service.understand(
        QueryUnderstandingRequest(
            "What about Germany?",
            context=QueryContext(
                conversation=(
                    {"role": "user", "content": "Tell me about maternity leave."},
                )
            ),
        )
    )

    assert result.strategy == QueryUnderstandingMode.LLM
    assert llm.called is True
