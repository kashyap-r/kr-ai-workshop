from rag_platform.context.token_counter import ApproximateTokenCounter


def test_empty_text_returns_zero() -> None:
    counter = ApproximateTokenCounter()

    assert counter.count("") == 0


def test_token_count_is_positive_for_non_empty_text() -> None:
    counter = ApproximateTokenCounter()

    assert counter.count("hello world") >= 1


def test_token_count_is_deterministic() -> None:
    counter = ApproximateTokenCounter()
    text = "This is deterministic test text."

    assert counter.count(text) == counter.count(text)
