"""Token counting implementations used by context assembly."""

from __future__ import annotations


class ApproximateTokenCounter:
    """Estimate token count using a lightweight character-based heuristic.

    This implementation is intentionally model-independent and is suitable
    for the initial RAG prototype. A model-specific tokenizer can be added
    later without changing the ContextAssembler contract.
    """

    def count(self, text: str) -> int:
        """Return an approximate token count for the supplied text."""

        if not text:
            return 0

        return max(1, len(text) // 4)
