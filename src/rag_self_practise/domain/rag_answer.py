from dataclasses import dataclass

from rag_self_practise.domain.retrieved_chunk import RetrievedChunk


@dataclass(frozen=True)
class RagAnswer:
    """An LLM-generated answer, together with the chunks it was grounded in."""

    answer: str
    sources: list[RetrievedChunk]
