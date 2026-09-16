from rag_platform.query.models import QueryUnderstandingMode, QueryUnderstandingRequest
from rag_platform.query.rule_based import RuleBasedQueryUnderstanding, normalize_query


def test_normalize_query() -> None:
    assert normalize_query("  What   is the policy ?  ") == "What is the policy?"


def test_rule_based_extracts_country_and_leave_type() -> None:
    result = RuleBasedQueryUnderstanding().understand(
        QueryUnderstandingRequest("How much maternity leave do employees get in Germany?")
    )

    assert result.intent == "policy_lookup"
    assert result.entities == {"country": "Germany", "leave_type": "maternity"}
    assert result.filters == {"country": "Germany"}
    assert result.strategy == QueryUnderstandingMode.RULE
    assert result.retrieval_query == result.normalized_query


def test_rule_based_detects_wfh() -> None:
    result = RuleBasedQueryUnderstanding().understand(
        QueryUnderstandingRequest("What is the WFH policy?")
    )

    assert result.intent == "policy_lookup"
    assert result.entities["topic"] == "work_from_home"


def test_rule_based_marks_complex_query_for_escalation() -> None:
    result = RuleBasedQueryUnderstanding().understand(
        QueryUnderstandingRequest("Compare maternity leave in Germany and Sweden.")
    )

    assert RuleBasedQueryUnderstanding.should_escalate(result, context_present=False)
