import argparse
import json
from pathlib import Path

import pymupdf4llm


def convert_pdf_to_json(pdf_path: str, json_path: str) -> None:
    pages = pymupdf4llm.to_markdown(pdf_path, page_chunks=True)

    entries = [
        {"content": page["text"], "pageNo": page["metadata"]["page_number"]}
        for page in pages
    ]

    Path(json_path).write_text(json.dumps(entries, indent=2), encoding="utf-8")
    print(f"Wrote {len(entries)} pages to {json_path}")


def main() -> None:
    parser = argparse.ArgumentParser(description="Convert a PDF into the pipeline's JSON format using pymupdf4llm.")
    parser.add_argument("pdf_path", help="Path to the input PDF file")
    parser.add_argument("json_path", help="Path to write the output JSON file")
    args = parser.parse_args()

    convert_pdf_to_json(args.pdf_path, args.json_path)


if __name__ == "__main__":
    main()
