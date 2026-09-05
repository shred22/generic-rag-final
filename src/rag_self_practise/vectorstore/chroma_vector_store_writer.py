import logging
from dataclasses import asdict

from langchain_chroma import Chroma
from langchain_openai import OpenAIEmbeddings

from rag_self_practise.domain import Chunk
from rag_self_practise.vectorstore.vector_store_writer import VectorStoreWriterInterface

logger = logging.getLogger(__name__)


class ChromaVectorStoreWriter(VectorStoreWriterInterface):
    """Embeds chunks with OpenAI and writes them into a persistent Chroma
    collection. Chunk IDs are derived deterministically from their metadata,
    and chunks whose ID is already present in the collection are skipped
    before embedding -- so re-running ingestion on the same document neither
    duplicates entries nor re-spends OpenAI credits on unchanged chunks."""

    def __init__(self, collection_name: str, persist_directory: str = "./chroma_db"):
        self._store = Chroma(
            collection_name=collection_name,
            embedding_function=OpenAIEmbeddings(model="text-embedding-3-small"),
            persist_directory=persist_directory,
        )

    def write(self, chunks: list[Chunk]) -> None:
        if not chunks:
            logger.info("No chunks to write")
            return

        new_chunks = self._filter_out_already_embedded(chunks)
        skipped_count = len(chunks) - len(new_chunks)
        if skipped_count:
            logger.info("Skipping %d chunks already present in the collection", skipped_count)

        if not new_chunks:
            logger.info("Nothing new to embed")
            return

        texts = [chunk.text for chunk in new_chunks]
        metadatas = [asdict(chunk.metadata) for chunk in new_chunks]
        ids = [self._build_chunk_id(chunk) for chunk in new_chunks]

        logger.info("Embedding and writing %d new chunks", len(new_chunks))
        self._store.add_texts(texts=texts, metadatas=metadatas, ids=ids)
        logger.info("Write complete")

    def _filter_out_already_embedded(self, chunks: list[Chunk]) -> list[Chunk]:
        all_ids = [self._build_chunk_id(chunk) for chunk in chunks]
        existing = self._store.get(ids=all_ids, include=[])
        existing_ids = set(existing["ids"])

        return [
            chunk
            for chunk, chunk_id in zip(chunks, all_ids)
            if chunk_id not in existing_ids
        ]

    def _build_chunk_id(self, chunk: Chunk) -> str:
        metadata = chunk.metadata
        return f"page-{metadata.page_no}-{metadata.block_type}-{metadata.chunk_index}"
