""" Recursive Document Chunker"""

from rag_platform.domain.identity import derive_chunk_id
from rag_platform.domain.models import DocumentChunk, ParsedDocument


class RecursiveChunker:
    """Split parsed documents into deterministic overlapping chunks"""
    VERSION = "recursive-v1"

    def __init__(self, *, chunk_size: int=1000, chunk_overlap: int = 150,) -> None:
        if chunk_size <= 0:
            raise ValueError("chunk_size must be positive!")
        if chunk_overlap < 0:
            raise ValueError("chunk_overalap cannot be negative!")
        if chunk_overlap >= chunk_size:
            raise ValueError("chunk_overlap must be smaller than chunk_size!")

        self.chunk_size = chunk_size
        self.chunk_overlap = chunk_overlap

    def chunk(self, document: ParsedDocument) -> list[DocumentChunk]:
        text = document.text

        if not text:
            return []

        chunks = self._split(text)

        results: list[DocumentChunk] = []

        search_start = 0

        for sequence_number, chunk_text in enumerate(chunks):
            start_offset = text.find(chunk_text, search_start)
            if start_offset == -1:
                raise ValueError("Unable to determine chunk offset.")

            end_offset = start_offset + len(chunk_text)

            results.append(
                DocumentChunk(
                    chunk_id=
                        derive_chunk_id(
                            document.id,
                            1,
                            self.VERSION,
                            sequence_number,
                            chunk_text,
                        ),
                    document_id=document.id,
                    document_version=1,
                    chunking_version=self.VERSION,
                    text=chunk_text,
                    metadata=document.metadata,
                    sequence_number=sequence_number,
                    start_offset=start_offset,
                    end_offset=end_offset,
                )
            )

            search_start = max(
                start_offset + 1,
                end_offset - self.chunk_overlap,
            )

        return results

    def _split(self, text: str) -> list[str]:
        """Split text into overlapping chunks."""
        chunks: list[str] = []

        start = 0

        while start < len(text):
            end = min(start + self.chunk_size, len(text))
            chunk = text[start:end]

            chunks.append(chunk)

            if end == len(text):
                break

            start = end - self.chunk_overlap

        return chunks
