from langchain_openai import ChatOpenAI

from rag_self_practise.domain import RagAnswer, RetrievedChunk
from rag_self_practise.rag.rag_answer_generator import RagAnswerGeneratorInterface
from rag_self_practise.vectorstore import RetrieverInterface

_SYSTEM_PROMPT = """You are a helpful assistant that answers questions using ONLY the context provided below.

Rules:
- Base your answer strictly on the given context. Do not use outside knowledge.
- If the context does not contain enough information to answer the question, say so clearly instead of guessing.
- Be concise and accurate.

Context:
{context}"""


class OpenAiRagAnswerGenerator(RagAnswerGeneratorInterface):
    """Retrieves relevant chunks and asks an OpenAI chat model to answer the
    question using only that context, so answers stay grounded in the
    source document rather than the model's general knowledge."""

    def __init__(self, retriever: RetrieverInterface, model: str = "gpt-4o-mini", top_k: int = 4):
        self._retriever = retriever
        self._llm = ChatOpenAI(model=model)
        self._top_k = top_k

    def answer(self, query: str) -> RagAnswer:
        sources = self._retriever.retrieve(query, top_k=self._top_k)

        system_prompt = _SYSTEM_PROMPT.format(context=self._build_context(sources))
        response = self._llm.invoke(
            [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": query},
            ]
        )

        return RagAnswer(answer=response.content, sources=sources)

    def _build_context(self, sources: list[RetrievedChunk]) -> str:
        if not sources:
            return "(no relevant context was found)"

        context_blocks = [
            f"[Page {source.chunk.metadata.page_no}]\n{source.chunk.text}" for source in sources
        ]
        return "\n\n---\n\n".join(context_blocks)
