from rag_self_practise.domain import TableBlock
from rag_self_practise.enrichers.table_context_enricher import TableContextEnricherInterface


class RowWiseTableContextEnricher(TableContextEnricherInterface):
    """Converts each table row into a "Column N: value" text block.

    The detected header row cannot be trusted as real column labels -- some
    tables (e.g. two-column glossary tables) have no true header, and the
    "header" is really just the first data row. To avoid ever silently
    dropping data, the header row is included as a data row too, and every
    row (including it) is labelled with generic positional column names.
    """

    def enrich(self, table: TableBlock) -> list[str]:
        all_rows = [table.headers, *table.rows]
        enriched_rows = [self._enrich_row(row) for row in all_rows]

        if table.caption:
            return [f"{table.caption}\n{row_text}" for row_text in enriched_rows]
        return enriched_rows

    def _enrich_row(self, row: list[str]) -> str:
        lines = [f"Column {position}: {value}" for position, value in enumerate(row, start=1)]
        return "\n".join(lines)
