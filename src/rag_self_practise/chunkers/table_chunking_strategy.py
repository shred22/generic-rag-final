from rag_self_practise.chunkers.chunking_strategy import ChunkingStrategy
from rag_self_practise.domain import Chunk, ChunkMetadata, ContentBlock, TableBlock
from rag_self_practise.enrichers import TableContextEnricherInterface


class TableChunkingStrategy(ChunkingStrategy):
    """Groups a table's enriched rows into chunks.

    Rows are packed together up to max_chunk_size so short rows don't each
    become their own tiny chunk, but a single row's enriched text is never
    split across chunks -- a row is the smallest unit that still preserves
    column/value context.
    """

    def __init__(self, enricher: TableContextEnricherInterface, max_chunk_size: int = 1000):
        self._enricher = enricher
        self._max_chunk_size = max_chunk_size

    def chunk(self, block: ContentBlock) -> list[Chunk]:
        if not isinstance(block, TableBlock):
            raise TypeError(f"TableChunkingStrategy cannot chunk {type(block).__name__}")

        enriched_rows = self._enricher.enrich(block)
        grouped_texts = self._group_rows(enriched_rows)

        return [
            Chunk(
                text=group_text,
                metadata=ChunkMetadata(
                    page_no=block.page_no,
                    block_type="table",
                    chunk_index=index,
                ),
            )
            for index, group_text in enumerate(grouped_texts)
        ]

    def _group_rows(self, enriched_rows: list[str]) -> list[str]:
        groups: list[str] = []
        current_group_rows: list[str] = []
        current_group_size = 0

        for row_text in enriched_rows:
            row_size = len(row_text)
            would_exceed_limit = current_group_size + row_size > self._max_chunk_size
            if current_group_rows and would_exceed_limit:
                groups.append("\n\n".join(current_group_rows))
                current_group_rows = []
                current_group_size = 0

            current_group_rows.append(row_text)
            current_group_size += row_size

        if current_group_rows:
            groups.append("\n\n".join(current_group_rows))

        return groups
