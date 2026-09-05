from abc import ABC, abstractmethod

from rag_self_practise.domain import TableBlock


class TableContextEnricherInterface(ABC):
    """Converts a table's rows into text that preserves column/value context."""

    @abstractmethod
    def enrich(self, table: TableBlock) -> list[str]:
        raise NotImplementedError
