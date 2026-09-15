from pathlib import Path

import pytest

from rag_platform.indexing import DocumentIndexState, IndexManifest


def test_manifest_round_trip(tmp_path: Path) -> None:
    path = tmp_path / "index_manifest.json"
    manifest = IndexManifest(
        index_version="index-v1",
        embedding_model="test-model",
        documents={
            "doc-1": DocumentIndexState(document_hash="abc", chunk_ids=["c1", "c2"]),
        },
    )

    manifest.save(path)
    loaded = IndexManifest.load(path, index_version="index-v1", embedding_model="test-model")

    assert loaded == manifest


def test_missing_manifest_returns_empty(tmp_path: Path) -> None:
    manifest = IndexManifest.load(
        tmp_path / "missing.json",
        index_version="index-v1",
        embedding_model="test-model",
    )

    assert manifest.documents == {}


def test_manifest_rejects_embedding_model_mismatch(tmp_path: Path) -> None:
    path = tmp_path / "index_manifest.json"
    IndexManifest.empty(index_version="index-v1", embedding_model="model-a").save(path)

    with pytest.raises(ValueError, match="embedding model"):
        IndexManifest.load(path, index_version="index-v1", embedding_model="model-b")
