from __future__ import annotations

import json
import os
from dataclasses import asdict, dataclass, field
from pathlib import Path
from tempfile import NamedTemporaryFile
from typing import Any


@dataclass(frozen=True)
class DocumentIndexState:
    """Persisted index state for one logical document."""

    document_hash: str
    chunk_ids: list[str] = field(default_factory=list)


@dataclass
class IndexManifest:
    """Persistent state used to reconcile the chunk corpus with the index."""

    index_version: str
    embedding_model: str
    documents: dict[str, DocumentIndexState] = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        return {
            "index_version": self.index_version,
            "embedding_model": self.embedding_model,
            "documents": {
                document_id: asdict(state)
                for document_id, state in sorted(self.documents.items())
            },
        }

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> IndexManifest:
        raw_documents = data.get("documents", {})
        if not isinstance(raw_documents, dict):
            raise ValueError("Manifest 'documents' must be an object.")

        documents: dict[str, DocumentIndexState] = {}
        for document_id, raw_state in raw_documents.items():
            if not isinstance(raw_state, dict) or "document_hash" not in raw_state:
                raise ValueError(f"Invalid manifest state for document {document_id!r}.")
            documents[str(document_id)] = DocumentIndexState(
                document_hash=str(raw_state["document_hash"]),
                chunk_ids=[str(chunk_id) for chunk_id in raw_state.get("chunk_ids", [])],
            )

        try:
            index_version = str(data["index_version"])
            embedding_model = str(data["embedding_model"])
        except KeyError as exc:
            raise ValueError(f"Manifest missing required field: {exc.args[0]}") from exc

        return cls(
            index_version=index_version,
            embedding_model=embedding_model,
            documents=documents,
        )

    @classmethod
    def empty(cls, *, index_version: str, embedding_model: str) -> IndexManifest:
        return cls(index_version=index_version, embedding_model=embedding_model)

    @classmethod
    def load(
        cls,
        path: Path,
        *,
        index_version: str,
        embedding_model: str,
    ) -> IndexManifest:
        if not path.exists():
            return cls.empty(index_version=index_version, embedding_model=embedding_model)

        with path.open("r", encoding="utf-8") as handle:
            raw_data = json.load(handle)

        if not isinstance(raw_data, dict):
            raise ValueError("Index manifest root must be a JSON object.")

        manifest = cls.from_dict(raw_data)
        if manifest.index_version != index_version:
            raise ValueError(
                f"Unsupported index manifest version: {manifest.index_version!r}; "
                f"expected {index_version!r}"
            )
        if manifest.embedding_model != embedding_model:
            raise ValueError(
                f"Manifest embedding model {manifest.embedding_model!r} does not "
                f"match configured model {embedding_model!r}"
            )
        return manifest

    def save(self, path: Path) -> None:
        """Atomically replace the manifest after successfully writing it."""
        path.parent.mkdir(parents=True, exist_ok=True)
        payload = json.dumps(self.to_dict(), indent=2, sort_keys=True) + "\n"

        with NamedTemporaryFile(
            mode="w",
            encoding="utf-8",
            dir=path.parent,
            prefix=f".{path.name}.",
            suffix=".tmp",
            delete=False,
        ) as handle:
            temp_path = Path(handle.name)
            try:
                handle.write(payload)
                handle.flush()
                os.fsync(handle.fileno())
            except Exception:
                temp_path.unlink(missing_ok=True)
                raise

        temp_path.replace(path)
