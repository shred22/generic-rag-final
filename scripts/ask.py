import argparse

from dotenv import load_dotenv

from rag_self_practise.rag import OpenAiRagAnswerGenerator
from rag_self_practise.vectorstore import ChromaRetriever


def main() -> None:
    load_dotenv()

    parser = argparse.ArgumentParser(description="Ask a question against a Chroma collection built by main.py.")
    parser.add_argument("collection_name", help="Name of the Chroma collection to search")
    parser.add_argument("query", help="Natural-language question")
    parser.add_argument("--top-k", type=int, default=4, help="Number of chunks to retrieve as context")
    args = parser.parse_args()

    retriever = ChromaRetriever(collection_name=args.collection_name)
    generator = OpenAiRagAnswerGenerator(retriever=retriever, top_k=args.top_k)

    result = generator.answer(args.query)

    print(result.answer)
    print()
    print("Sources:")
    for source in result.sources:
        print(f"  page {source.chunk.metadata.page_no} (score={source.score:.4f})")


if __name__ == "__main__":
    main()
