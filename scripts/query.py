import argparse

from dotenv import load_dotenv

from rag_self_practise.vectorstore import ChromaRetriever


def main() -> None:
    load_dotenv()

    parser = argparse.ArgumentParser(description="Query a Chroma collection built by main.py.")
    parser.add_argument("collection_name", help="Name of the Chroma collection to search")
    parser.add_argument("query", help="Natural-language question")
    parser.add_argument("--top-k", type=int, default=4, help="Number of results to return")
    args = parser.parse_args()

    retriever = ChromaRetriever(collection_name=args.collection_name)
    results = retriever.retrieve(args.query, top_k=args.top_k)

    for result in results:
        print(f"score={result.score:.4f} {result.chunk.metadata}")
        print(result.chunk.text)
        print("---")


if __name__ == "__main__":
    main()
