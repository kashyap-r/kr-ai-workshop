import re
from collections.abc import Iterable

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

_COUNTRIES = ("germany", "sweden", "india")
_LEAVE_TERMS = {
    "maternity": ("maternity", "maternity leave"),
    "parental": ("parental", "parental leave"),
    "annual": ("annual leave", "vacation leave", "holiday leave"),
    "sick": ("sick leave", "sick"),
}
_TOPIC_TERMS = {
    "work_from_home": ("work from home", "wfh", "remote work", "working remotely", "hybrid work"),
    "notice_period": ("notice period", "notice"),
    "benefits": ("benefit", "benefits"),
    "employment": ("employment", "contract", "employment contract"),
}


def normalize_query(query: str) -> str:
    normalized = re.sub(r"\s+", " ", query.strip())
    normalized = re.sub(r"\s+([?.!,;:])", r"\1", normalized)
    return normalized


def _contains_any(text: str, terms: Iterable[str]) -> bool:
    return any(term in text for term in terms)


def _extract_entities(query: str) -> dict[str, str]:
    text = query.lower()
    entities: dict[str, str] = {}

    for country in _COUNTRIES:
        if re.search(rf"\b{re.escape(country)}\b", text):
            entities["country"] = country.title()
            break

    for leave_type, terms in _LEAVE_TERMS.items():
        if _contains_any(text, terms):
            entities["leave_type"] = leave_type
            break

    if _contains_any(text, _TOPIC_TERMS["work_from_home"]):
        entities["topic"] = "work_from_home"
    elif _contains_any(text, _TOPIC_TERMS["notice_period"]):
        entities["topic"] = "notice_period"
    elif _contains_any(text, _TOPIC_TERMS["benefits"]):
        entities["topic"] = "benefits"
    elif _contains_any(text, _TOPIC_TERMS["employment"]):
        entities["topic"] = "employment"

    return entities


def _classify_intent(query: str, entities: dict[str, str]) -> str:
    text = query.lower()

    if "profile" in text or "who is" in text or "employee details" in text:
        return "employee_lookup"
    if entities.get("topic") == "notice_period" or "notice period" in text:
        return "employment_terms"
    if entities.get("topic") == "benefits" or "benefit" in text:
        return "benefit_lookup"
    if any(key in entities for key in ("leave_type", "topic")):
        return "policy_lookup"
    if any(word in text for word in ("policy", "rule", "rules", "allowed", "entitled")):
        return "policy_lookup"
    return "general_information"


def _is_simple_query(query: str, entities: dict[str, str]) -> bool:
    text = query.lower()
    word_count = len(text.split())
    question_count = text.count("?")
    has_comparison = any(
        term in text
        for term in ("compare", "comparison", "versus", " vs ", "difference"))
    has_multiple_parts = any(
        term in text
        for term in (" and ", " as well as ", "also ")) and word_count > 10
    has_ellipsis = "..." in text
    return (
        word_count <= 15
        and question_count <= 1
        and not has_comparison
        and not has_multiple_parts
        and not has_ellipsis
        and bool(entities)
    )


class RuleBasedQueryUnderstanding:
    """Fast, deterministic first-pass query understanding."""

    def understand(self, request: QueryUnderstandingRequest) -> QueryUnderstandingResult:
        normalized = normalize_query(request.query)
        entities = _extract_entities(normalized)
        intent = _classify_intent(normalized, entities)
        filters = {"country": entities["country"]} if "country" in entities else {}

        logger.info(
            "query_understanding_rule_completed",
            extra={
                "query_length": len(normalized),
                "intent": intent,
                "entity_count": len(entities),
                "filter_count": len(filters),
                "simple_query": _is_simple_query(normalized, entities),
            },
        )

        return QueryUnderstandingResult(
            original_query=request.query,
            normalized_query=normalized,
            intent=intent,
            entities=entities,
            filters=filters,
            strategy=QueryUnderstandingMode.RULE,
        )

    @staticmethod
    def should_escalate(result: QueryUnderstandingResult, context_present: bool) -> bool:
        query = result.normalized_query.lower()
        word_count = len(query.split())
        has_comparison = any(
            term in query
            for term in ("compare", "comparison", "versus", " vs ", "difference"))
        has_multiple_questions = query.count("?") > 1
        has_follow_up = query in {
            "what about germany?",
            "what about india?",
            "what about sweden?",
        } or query.startswith(
            ("what about ", "how about ", "and what about ", "is it ", "how long is it")
        )
        return (
            context_present
            or has_comparison
            or has_multiple_questions
            or has_follow_up
            or word_count > 20
            or not result.entities
        )
