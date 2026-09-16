from typing import cast

import pytest

from rag_platform.domain.models import DocumentChunk
from rag_platform.domain.types import ChunkID, DocumentID
from rag_platform.retrieval import BM25IndexStore, BM25Retriever, tokenize


def chunk(chunk_id: str, text: str) -> DocumentChunk:
    return DocumentChunk(
        chunk_id=ChunkID(chunk_id),
        document_id=DocumentID("doc-1"),
        document_version=1,
        chunking_version="recursive-v1",
        text=text,
        metadata={},
        sequence_number=0,
        start_offset=0,
        end_offset=len(text),
    )


def test_tokenizer_preserves_identifiers() -> None:
    tokens = tokenize("EMP-1042 uses WFH_policy in Germany")
    assert "emp-1042" in tokens
    assert "wfh_policy" in tokens


def test_bm25_retrieves_exact_identifier() -> None:
    index = BM25IndexStore()
    index.upsert([
        chunk("c1", "Employee EMP-1042 is based in Germany."),
        chunk("c2", "Remote work policy for India employees."),
    ])
    results = BM25Retriever(index).retrieve("EMP-1042", top_k=2)
    assert [str(result.chunk.chunk_id) for result in results] == ["c1"]


def test_bm25_ranks_multiple_matching_terms() -> None:
    index = BM25IndexStore()
    index.upsert([
        chunk("c1", "Germany maternity leave policy applies to employees."),
        chunk("c2", "Germany employee handbook."),
        chunk("c3", "India remote work policy."),
    ])
    results = BM25Retriever(index).retrieve("Germany maternity leave policy", top_k=3)
    assert [str(result.chunk.chunk_id) for result in results][:2] == ["c1", "c2"]


def test_empty_index_and_empty_text_are_safe() -> None:
    empty = BM25Retriever(BM25IndexStore())
    assert empty.retrieve("anything") == []
    index = BM25IndexStore()
    index.upsert([chunk("c1", ""), chunk("c2", "")])
    assert BM25Retriever(index).retrieve("anything") == []


def test_empty_and_non_matching_queries() -> None:
    index = BM25IndexStore()
    index.upsert([chunk("c1", "remote work")])
    retriever = BM25Retriever(index)
    assert retriever.retrieve("quantum physics") == []
    with pytest.raises(ValueError):
        retriever.retrieve(" ")


def test_index_upsert_delete_and_persistence(tmp_path) -> None:
    path = tmp_path / "bm25.json"
    index = BM25IndexStore(path)
    index.upsert([chunk("c1", "remote work"), chunk("c2", "leave policy")])
    index.save()

    loaded = BM25IndexStore(path)
    assert {str(c.chunk_id) for c in loaded.chunks} == {"c1", "c2"}
    loaded.delete(["c1"])
    loaded.save()
    reloaded = BM25IndexStore(path)
    assert [str(c.chunk_id) for c in reloaded.chunks] == ["c2"]


def test_duplicate_upsert_batch_is_rejected() -> None:
    index = BM25IndexStore()
    with pytest.raises(ValueError, match="Duplicate chunk ID"):
        index.upsert([chunk("c1", "one"), chunk("c1", "two")])
