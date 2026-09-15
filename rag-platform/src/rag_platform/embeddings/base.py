""" Embeddig model abstraction """
from collections.abc import Sequence
from typing import Protocol


class EmbeddingModel (Protocol):
    def embed(self, texts: Sequence[str]) -> Sequence[Sequence[float]]:
        """Geberate one embedding vector for each input text."""
        ...
