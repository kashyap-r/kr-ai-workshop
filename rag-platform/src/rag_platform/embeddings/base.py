""" Embeddig model abstraction """
from typing import Protocol
from collections.abc import Sequence

class EmbeddingModel (Protocol):
    def embed(self, texts: Sequence[str]) -> Sequence[Sequence[float]]:
        """Geberate one embedding vector for each input text."""
        ...
