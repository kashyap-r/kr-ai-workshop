from rag_platform.logging import configure_logging
from rag_platform.query.llm import LLMQueryUnderstanding
from rag_platform.query.models import (
    QueryUnderstandingMode,
    QueryUnderstandingRequest,
    QueryUnderstandingResult,
)
from rag_platform.query.rule_based import RuleBasedQueryUnderstanding

logger = configure_logging(
    logger_name=__name__,
    log_file="logs/query_understanding.log",
)


class HybridQueryUnderstanding:
    """Route simple queries to rules and complex queries to an LLM."""

    def __init__(
        self,
        rule_based: RuleBasedQueryUnderstanding | None = None,
        llm: LLMQueryUnderstanding | None = None,
    ) -> None:
        self._rule_based = rule_based or RuleBasedQueryUnderstanding()
        self._llm = llm or LLMQueryUnderstanding()

    def understand(self, request: QueryUnderstandingRequest) -> QueryUnderstandingResult:
        if request.mode == QueryUnderstandingMode.RULE:
            return self._rule_based.understand(request)

        if request.mode == QueryUnderstandingMode.LLM:
            return self._llm.understand(request)

        rule_result = self._rule_based.understand(request)
        should_use_llm = self._rule_based.should_escalate(
            rule_result,
            context_present=bool(request.context and request.context.conversation),
        )

        if not should_use_llm:
            return rule_result

        logger.info(
            "query_understanding_escalating_to_llm",
            extra={
                "reason": "complex_or_ambiguous_query",
                "intent": rule_result.intent,
            },
        )

        if not self._llm.available:
            logger.info(
                "query_understanding_llm_unavailable",
                extra={"fallback": "rule_based"},
            )
            return QueryUnderstandingResult(
                original_query=rule_result.original_query,
                normalized_query=rule_result.normalized_query,
                rewritten_query=rule_result.rewritten_query,
                intent=rule_result.intent,
                entities=rule_result.entities,
                filters=rule_result.filters,
                expanded_queries=rule_result.expanded_queries,
                strategy=QueryUnderstandingMode.RULE,
                fallback_used=True,
            )

        try:
            return self._llm.understand(request)
        except RuntimeError:
            logger.warning(
                "query_understanding_llm_fallback",
                extra={"fallback": "rule_based"},
            )
            return QueryUnderstandingResult(
                original_query=rule_result.original_query,
                normalized_query=rule_result.normalized_query,
                rewritten_query=rule_result.rewritten_query,
                intent=rule_result.intent,
                entities=rule_result.entities,
                filters=rule_result.filters,
                expanded_queries=rule_result.expanded_queries,
                strategy=QueryUnderstandingMode.RULE,
                fallback_used=True,
            )
