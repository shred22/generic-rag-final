import sys
from pathlib import Path

from dotenv import load_dotenv

from rag_self_practise.chunkers import ProseChunkingStrategy, TableChunkingStrategy
from rag_self_practise.domain import ProseBlock, TableBlock
from rag_self_practise.enrichers import RowWiseTableContextEnricher
from rag_self_practise.loaders import JsonDocumentLoader
from rag_self_practise.pipeline import DocumentProcessingPipeline
from rag_self_practise.segmenters import MarkdownContentSegmenter
from rag_self_practise.vectorstore import ChromaVectorStoreWriter


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

    if len(sys.argv) != 2:
        print("Usage: uv run main.py <path-to-json-file>")
        sys.exit(1)

    json_path = sys.argv[1]
    collection_name = Path(json_path).stem

    pipeline = build_pipeline()
    chunks = pipeline.process(json_path)
    print(f"Produced {len(chunks)} chunks")

    writer = ChromaVectorStoreWriter(collection_name=collection_name)
    writer.write(chunks)
    print(f"Wrote {len(chunks)} chunks to Chroma collection '{collection_name}'")


if __name__ == "__main__":
    main()
