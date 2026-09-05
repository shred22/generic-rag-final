import json
from pathlib import Path

from rag_self_practise.domain import Page


class JsonDocumentLoader:
    """Reads a pymupdf4llm-style JSON file and parses it into Page objects."""

    def load(self, file_path: str) -> list[Page]:
        raw_text = Path(file_path).read_text(encoding="utf-8")
        raw_entries = json.loads(raw_text)

        if not isinstance(raw_entries, list):
            raise ValueError(
                f"Expected a JSON array at the top level, got {type(raw_entries).__name__}"
            )

        return [self._to_page(entry, index) for index, entry in enumerate(raw_entries)]

    def _to_page(self, entry: dict, index: int) -> Page:
        if "content" not in entry or "pageNo" not in entry:
            raise ValueError(
                f"Entry at index {index} is missing 'content' or 'pageNo': {entry}"
            )

        return Page(content=entry["content"], page_no=entry["pageNo"])
