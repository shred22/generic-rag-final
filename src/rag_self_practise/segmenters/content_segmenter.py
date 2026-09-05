from abc import ABC, abstractmethod

from rag_self_practise.domain import ContentBlock, Page


class ContentSegmenterInterface(ABC):
    """Splits a page's raw content into an ordered list of content blocks."""

    @abstractmethod
    def segment(self, page: Page) -> list[ContentBlock]:
        raise NotImplementedError
