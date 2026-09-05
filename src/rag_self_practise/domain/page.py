from dataclasses import dataclass


@dataclass(frozen=True)
class Page:
    """One page of PDF content, as extracted by pymupdf4llm."""

    content: str
    page_no: int
