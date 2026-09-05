import logging

from dotenv import load_dotenv

from rag_self_practise.chunkers import ProseChunkingStrategy, TableChunkingStrategy
from rag_self_practise.config import TomlConfigLoader
from rag_self_practise.domain import ProseBlock, TableBlock
from rag_self_practise.enrichers import RowWiseTableContextEnricher
from rag_self_practise.loaders import JsonDocumentLoader
from rag_self_practise.logging_config import configure_logging
from rag_self_practise.pipeline import DocumentProcessingPipeline
from rag_self_practise.segmenters import MarkdownContentSegmenter
from rag_self_practise.vectorstore import ChromaVectorStoreWriter

logger = logging.getLogger(__name__)


def build_pipeline() -> DocumentProcessingPipeline:
    return DocumentProcessingPipeline(
        loader=JsonDocumentLoader(),
        segmenter=MarkdownContentSegmenter(),
        strategies_by_block_type={
            ProseBlock: ProseChunkingStrategy(),
            TableBlock: TableChunkingStrategy(RowWiseTableContextEnricher()),
        },
    )


def main():
    load_dotenv()
    configure_logging()

    config = TomlConfigLoader().load("config/config.toml")
    logger.info("Starting ingestion for '%s' into collection '%s'", config.json_path, config.collection_name)

    pipeline = build_pipeline()
    chunks = pipeline.process(config.json_path)

    writer = ChromaVectorStoreWriter(collection_name=config.collection_name)
    writer.write(chunks)
    logger.info("Ingestion finished: %d chunks in collection '%s'", len(chunks), config.collection_name)


if __name__ == "__main__":
    main()
