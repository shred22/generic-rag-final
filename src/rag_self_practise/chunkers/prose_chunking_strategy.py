from langchain_text_splitters import RecursiveCharacterTextSplitter

from rag_self_practise.chunkers.chunking_strategy import ChunkingStrategy
from rag_self_practise.domain import Chunk, ChunkMetadata, ContentBlock, ProseBlock


class ProseChunkingStrategy(ChunkingStrategy):
    """Splits prose text into overlapping chunks using LangChain's
    RecursiveCharacterTextSplitter."""

    def __init__(self, chunk_size: int = 1000, chunk_overlap: int = 150):
        self._splitter = RecursiveCharacterTextSplitter(
            chunk_size=chunk_size,
            chunk_overlap=chunk_overlap,
        )

    def chunk(self, block: ContentBlock) -> list[Chunk]:
        if not isinstance(block, ProseBlock):
            raise TypeError(f"ProseChunkingStrategy cannot chunk {type(block).__name__}")

        text_pieces = self._splitter.split_text(block.text)

        return [
            Chunk(
                text=text_piece,
                metadata=ChunkMetadata(
                    page_no=block.page_no,
                    block_type="prose",
                    chunk_index=index,
                ),
            )
            for index, text_piece in enumerate(text_pieces)
        ]
