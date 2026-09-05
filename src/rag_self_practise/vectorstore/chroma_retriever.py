from langchain_chroma import Chroma
from langchain_core.documents import Document
from langchain_openai import OpenAIEmbeddings

from rag_self_practise.domain import Chunk, ChunkMetadata, RetrievedChunk
from rag_self_practise.vectorstore.retriever import RetrieverInterface


class ChromaRetriever(RetrieverInterface):
    """Finds the chunks most relevant to a query within a single Chroma
    collection, using OpenAI embeddings for the query."""

    def __init__(self, collection_name: str, persist_directory: str = "./chroma_db"):
        self._store = Chroma(
            collection_name=collection_name,
            embedding_function=OpenAIEmbeddings(model="text-embedding-3-small"),
            persist_directory=persist_directory,
        )

    def retrieve(self, query: str, top_k: int = 4) -> list[RetrievedChunk]:
        results = self._store.similarity_search_with_score(query, k=top_k)

        return [
            RetrievedChunk(chunk=self._to_chunk(document), score=score)
            for document, score in results
        ]

    def _to_chunk(self, document: Document) -> Chunk:
        metadata = ChunkMetadata(
            page_no=document.metadata["page_no"],
            block_type=document.metadata["block_type"],
            chunk_index=document.metadata["chunk_index"],
        )
        return Chunk(text=document.page_content, metadata=metadata)
