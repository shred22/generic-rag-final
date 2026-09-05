import logging
from dataclasses import replace

from rag_self_practise.chunkers import ChunkingStrategy
from rag_self_practise.domain import Chunk, ContentBlock, Page
from rag_self_practise.loaders import JsonDocumentLoader
from rag_self_practise.segmenters import ContentSegmenterInterface

logger = logging.getLogger(__name__)


class DocumentProcessingPipeline:
    """Coordinates the full pipeline: JSON file -> chunks ready for embedding.

    Contains no parsing/chunking logic itself -- it only sequences calls to
    the loader, segmenter, and the chunking strategy registered for each
    content block type.
    """

    def __init__(
        self,
        loader: JsonDocumentLoader,
        segmenter: ContentSegmenterInterface,
        strategies_by_block_type: dict[type, ChunkingStrategy],
    ):
        self._loader = loader
        self._segmenter = segmenter
        self._strategies_by_block_type = strategies_by_block_type

    def process(self, json_path: str) -> list[Chunk]:
        logger.info("Loading pages from %s", json_path)
        pages = self._loader.load(json_path)
        logger.info("Loaded %d pages", len(pages))

        all_chunks: list[Chunk] = []
        for page in pages:
            all_chunks.extend(self._process_page(page))

        logger.info("Produced %d chunks from %d pages", len(all_chunks), len(pages))
        return all_chunks

    def _process_page(self, page: Page) -> list[Chunk]:
        blocks = self._segmenter.segment(page)
        logger.debug("Page %d segmented into %d blocks", page.page_no, len(blocks))

        page_chunks: list[Chunk] = []
        for block in blocks:
            page_chunks.extend(self._chunk_block(block))

        # chunk_index is only unique within a single block's own strategy call
        # (each ChunkingStrategy starts counting from 0). A page can contain
        # multiple blocks of the same type (e.g. prose before AND after a
        # table), so renumber here to make chunk_index unique per page.
        return [
            Chunk(text=chunk.text, metadata=replace(chunk.metadata, chunk_index=index))
            for index, chunk in enumerate(page_chunks)
        ]

    def _chunk_block(self, block: ContentBlock) -> list[Chunk]:
        strategy = self._strategies_by_block_type.get(type(block))
        if strategy is None:
            raise ValueError(f"No chunking strategy registered for block type {type(block).__name__}")

        return strategy.chunk(block)
