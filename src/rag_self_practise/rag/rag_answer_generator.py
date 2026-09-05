from abc import ABC, abstractmethod

from rag_self_practise.domain import RagAnswer


class RagAnswerGeneratorInterface(ABC):
    """Answers a natural-language question using retrieved context."""

    @abstractmethod
    def answer(self, query: str) -> RagAnswer:
        raise NotImplementedError
