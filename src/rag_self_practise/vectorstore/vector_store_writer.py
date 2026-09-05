from abc import ABC, abstractmethod

from rag_self_practise.domain import Chunk


class VectorStoreWriterInterface(ABC):
    """Writes chunks into a vector store so they can later be retrieved."""

    @abstractmethod
    def write(self, chunks: list[Chunk]) -> None:
        raise NotImplementedError
