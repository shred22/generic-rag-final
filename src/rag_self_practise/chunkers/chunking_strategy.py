from abc import ABC, abstractmethod

from rag_self_practise.domain import Chunk, ContentBlock


class ChunkingStrategy(ABC):
    """Splits one content block into embedding-ready chunks."""

    @abstractmethod
    def chunk(self, block: ContentBlock) -> list[Chunk]:
        raise NotImplementedError
