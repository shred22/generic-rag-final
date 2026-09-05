from abc import ABC, abstractmethod

from rag_self_practise.domain import RetrievedChunk


class RetrieverInterface(ABC):
    """Finds the chunks most relevant to a natural-language query."""

    @abstractmethod
    def retrieve(self, query: str, top_k: int = 4) -> list[RetrievedChunk]:
        raise NotImplementedError
