from collections.abc import Sequence

from sentence_transformers import SentenceTransformer


class SentenceTransformerEmbeddingModel:
    """Embedding implementation backed by Sentence Transformers."""

    def __init__(self, model_name: str) -> None:
        self.model_name = model_name
        self._model = SentenceTransformer(model_name)

    def embed(
        self,
        texts: Sequence[str],
    ) -> list[list[float]]:
        if not texts:
            return []

        embeddings = self._model.encode(
            list(texts),
            convert_to_numpy=True,
            show_progress_bar=False,
        )

        return embeddings.tolist()
