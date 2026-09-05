from dataclasses import dataclass

from rag_self_practise.domain.chunk import Chunk


@dataclass(frozen=True)
class RetrievedChunk:
    """A chunk returned by a similarity search, paired with its relevance score."""

    chunk: Chunk
    score: float
