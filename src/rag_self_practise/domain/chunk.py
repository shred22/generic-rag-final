from dataclasses import dataclass


@dataclass(frozen=True)
class ChunkMetadata:
    """Traces a chunk back to the page and block it was produced from."""

    page_no: int
    block_type: str
    chunk_index: int


@dataclass(frozen=True)
class Chunk:
    text: str
    metadata: ChunkMetadata
