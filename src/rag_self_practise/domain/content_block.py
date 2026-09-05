from abc import ABC
from dataclasses import dataclass


@dataclass(frozen=True)
class ContentBlock(ABC):
    """A segment of a page's content, either prose or a table."""

    page_no: int


@dataclass(frozen=True)
class ProseBlock(ContentBlock):
    text: str


@dataclass(frozen=True)
class TableBlock(ContentBlock):
    headers: list[str]
    rows: list[list[str]]
    caption: str | None
