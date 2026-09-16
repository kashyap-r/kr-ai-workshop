from collections.abc import Sequence
from typing import cast

from rag_platform.domain.models import ChunkID, DocumentChunk, DocumentID
from rag_platform.indexing import Indexer, IndexManifest


class FakeEmbeddingModel:
    def __init__(self) -> None:
        self.calls: list[list[str]] = []

    def embed(self, texts: Sequence[str]) -> Sequence[Sequence[float]]:
        values = list(texts)
        self.calls.append(values)
        return [[float(index), 1.0] for index, _ in enumerate(values, start=1)]


class FakeVectorStore:
    def __init__(self) -> None:
        self.upserts: list[list[str]] = []
        self.deletes: list[list[str]] = []
        self.delete_all_calls = 0

    def upsert(
            self,
            chunks: Sequence[DocumentChunk],
            embeddings: Sequence[Sequence[float]]) -> None:
        assert len(chunks) == len(embeddings)
        self.upserts.append([str(chunk.chunk_id) for chunk in chunks])

    def delete(self, ids: Sequence[str]) -> None:
        self.deletes.append([str(chunk_id) for chunk_id in ids])

    def delete_all(self) -> None:
        self.delete_all_calls += 1

    def query(self, embedding: Sequence[float], *, top_k: int):
        return []


def chunk(document_id: str, chunk_id: str, sequence: int, text: str) -> DocumentChunk:
    return DocumentChunk(
        chunk_id=cast(ChunkID, chunk_id),
        document_id=cast(DocumentID, document_id),
        document_version=1,
        chunking_version="recursive-v1",
        text=text,
        metadata={},
        sequence_number=sequence,
        start_offset=sequence * 10,
        end_offset=sequence * 10 + len(text),
    )


def make_indexer() -> tuple[Indexer, FakeEmbeddingModel, FakeVectorStore]:
    embedder = FakeEmbeddingModel()
    store = FakeVectorStore()
    indexer = Indexer(
        embedding_model=embedder,
        vector_store=store,
        embedding_model_name="test-model",
    )
    return indexer, embedder, store


def test_new_document_is_embedded_and_upserted() -> None:
    indexer, embedder, store = make_indexer()
    manifest = IndexManifest.empty(index_version="index-v1", embedding_model="test-model")
    docs = {"doc-1": [chunk("doc-1", "c1", 0, "hello")]}

    result = indexer.synchronize(docs, manifest)

    assert result.documents_new == 1
    assert result.chunks_indexed == 1
    assert len(embedder.calls) == 1
    assert store.upserts == [["c1"]]
    assert manifest.documents["doc-1"].chunk_ids == ["c1"]


def test_unchanged_document_is_skipped() -> None:
    indexer, embedder, store = make_indexer()
    docs = {"doc-1": [chunk("doc-1", "c1", 0, "hello")]}
    manifest = IndexManifest.empty(index_version="index-v1", embedding_model="test-model")
    manifest.documents["doc-1"] = __import__(
                "rag_platform.indexing",
                fromlist=["DocumentIndexState"]).DocumentIndexState(
                    document_hash=indexer.document_hash(docs["doc-1"]), chunk_ids=["c1"]
    )

    result = indexer.synchronize(docs, manifest)

    assert result.documents_unchanged == 1
    assert result.embeddings_generated == 0
    assert embedder.calls == []
    assert store.upserts == []
    assert store.deletes == []


def test_changed_document_deletes_old_chunks_then_reindexes() -> None:
    indexer, embedder, store = make_indexer()
    old_docs = {"doc-1": [chunk("doc-1", "old-1", 0, "old text")]}
    new_docs = {"doc-1": [chunk("doc-1", "new-1", 0, "new text")]}
    manifest = IndexManifest.empty(index_version="index-v1", embedding_model="test-model")
    from rag_platform.indexing import DocumentIndexState
    manifest.documents["doc-1"] = DocumentIndexState(
        document_hash=indexer.document_hash(old_docs["doc-1"]), chunk_ids=["old-1"]
    )

    result = indexer.synchronize(new_docs, manifest)

    assert result.documents_changed == 1
    assert store.deletes == [["old-1"]]
    assert store.upserts == [["new-1"]]
    assert len(embedder.calls) == 1
    assert manifest.documents["doc-1"].chunk_ids == ["new-1"]


def test_deleted_document_is_removed_from_index_and_manifest() -> None:
    indexer, _, store = make_indexer()
    manifest = IndexManifest.empty(index_version="index-v1", embedding_model="test-model")
    from rag_platform.indexing import DocumentIndexState
    manifest.documents["doc-1"] = DocumentIndexState(document_hash="hash", chunk_ids=["c1", "c2"])

    result = indexer.synchronize({}, manifest)

    assert result.documents_deleted == 1
    assert result.chunks_deleted == 2
    assert store.deletes == [["c1", "c2"]]
    assert "doc-1" not in manifest.documents


def test_empty_document_can_be_indexed_without_embedding() -> None:
    indexer, embedder, store = make_indexer()
    manifest = IndexManifest.empty(index_version="index-v1", embedding_model="test-model")

    result = indexer.synchronize({"doc-1": []}, manifest)

    assert result.documents_new == 1
    assert result.chunks_indexed == 0
    assert embedder.calls == []
    assert store.upserts == []
    assert manifest.documents["doc-1"].chunk_ids == []
