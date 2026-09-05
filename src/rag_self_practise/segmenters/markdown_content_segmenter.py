import re

from rag_self_practise.domain import ContentBlock, Page, ProseBlock, TableBlock
from rag_self_practise.segmenters.content_segmenter import ContentSegmenterInterface

_TABLE_ROW_PATTERN = re.compile(r"^\s*\|.*\|\s*$")
_TABLE_SEPARATOR_PATTERN = re.compile(r"^\s*\|?\s*:?-+:?\s*(\|\s*:?-+:?\s*)*\|?\s*$")


class MarkdownContentSegmenter(ContentSegmenterInterface):
    """Detects Markdown pipe-tables within a page's content and separates
    them from surrounding prose, so each can be chunked differently."""

    def segment(self, page: Page) -> list[ContentBlock]:
        lines = page.content.splitlines()
        blocks: list[ContentBlock] = []
        prose_lines: list[str] = []
        index = 0

        while index < len(lines):
            if self._is_table_start(lines, index):
                self._flush_prose(blocks, prose_lines, page.page_no)
                table_lines, index = self._consume_table_lines(lines, index)
                blocks.append(self._parse_table(table_lines, page.page_no, prose_lines))
                prose_lines = []
            else:
                prose_lines.append(lines[index])
                index += 1

        self._flush_prose(blocks, prose_lines, page.page_no)
        return blocks

    def _is_table_start(self, lines: list[str], index: int) -> bool:
        if not _TABLE_ROW_PATTERN.match(lines[index]):
            return False
        if index + 1 >= len(lines):
            return False
        return bool(_TABLE_SEPARATOR_PATTERN.match(lines[index + 1]))

    def _consume_table_lines(self, lines: list[str], start_index: int) -> tuple[list[str], int]:
        index = start_index
        table_lines = []
        while index < len(lines) and _TABLE_ROW_PATTERN.match(lines[index]):
            table_lines.append(lines[index])
            index += 1
        return table_lines, index

    def _parse_table(self, table_lines: list[str], page_no: int, preceding_prose: list[str]) -> TableBlock:
        header_line, _separator_line, *row_lines = table_lines
        headers = self._split_row(header_line)
        rows = [self._split_row(row_line) for row_line in row_lines]
        caption = self._extract_caption(preceding_prose)
        return TableBlock(page_no=page_no, headers=headers, rows=rows, caption=caption)

    def _split_row(self, row_line: str) -> list[str]:
        trimmed = row_line.strip().strip("|")
        cells = trimmed.split("|")
        return [self._clean_cell(cell) for cell in cells]

    def _clean_cell(self, cell: str) -> str:
        return cell.replace("<br>", " ").strip()

    def _extract_caption(self, preceding_prose: list[str]) -> str | None:
        for line in reversed(preceding_prose):
            if line.strip():
                return line.strip()
        return None

    def _flush_prose(self, blocks: list[ContentBlock], prose_lines: list[str], page_no: int) -> None:
        text = "\n".join(prose_lines).strip()
        if text:
            blocks.append(ProseBlock(page_no=page_no, text=text))
