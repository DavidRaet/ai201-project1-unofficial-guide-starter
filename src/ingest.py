import json
import re
from pathlib import Path

import pdfplumber

from src.config import DATA_DIR, DOCUMENT_METADATA, DOCUMENTS_DIR, OUTPUT_PATH


def extract_pdf_text(path: Path) -> str:
    with pdfplumber.open(path) as pdf:
        pages = [page.extract_text() or "" for page in pdf.pages]
    return "\n".join(pages)


def clean_text(text: str) -> str:
    # Fix missing spaces at sentence boundaries created by PDF line-wrap (e.g. "correlates.And")
    text = re.sub(r"([a-z])\.([A-Z])", r"\1. \2", text)
    # Collapse runs of whitespace/newlines to single spaces, then strip
    text = re.sub(r"[ \t]+", " ", text)
    text = re.sub(r"\n{2,}", "\n", text)
    return text.strip()


def _parse_year(block: str) -> int | None:
    m = re.search(r"year:.*?(\d{4})", block, re.IGNORECASE)
    return int(m.group(1)) if m else None


def _parse_course_code(block: str) -> str | None:
    # Matches "CMPU-101", "CMPU 101", "CMPU-101-", "CMPU101"
    m = re.search(r"CMPU\s*-?\s*(\d{3})", block, re.IGNORECASE)
    return f"CMPU-{m.group(1)}" if m else None


def _strip_review_metadata(block: str) -> str:
    # Remove the trailing "year: ..." line
    text = re.sub(r"\n?year:.*", "", block, flags=re.IGNORECASE)
    return clean_text(text)


def parse_rmp_reviews(text: str, base_meta: dict) -> list[dict]:
    blocks = re.findall(r'"""(.*?)"""', text, re.DOTALL)
    records = []
    for block in blocks:
        course_code = _parse_course_code(block)
        year = _parse_year(block)
        review_text = _strip_review_metadata(block)
        if not review_text:
            continue
        metadata = {**base_meta}
        if course_code:
            metadata["course_code"] = course_code
        if year:
            metadata["approximate_year"] = year
        records.append({"text": review_text, "metadata": metadata})
    return records


def parse_single_document(text: str, base_meta: dict) -> list[dict]:
    return [{"text": clean_text(text), "metadata": {**base_meta}}]


def ingest_documents(documents_dir: Path = DOCUMENTS_DIR) -> list[dict]:
    records = []
    for filename, base_meta in DOCUMENT_METADATA.items():
        path = documents_dir / filename
        if not path.exists():
            print(f"WARNING: {filename} not found, skipping.")
            continue
        text = extract_pdf_text(path)
        if base_meta["source"] == "rmp":
            records.extend(parse_rmp_reviews(text, base_meta))
        else:
            records.extend(parse_single_document(text, base_meta))
    return records


def save_records(records: list[dict], output_path: Path = OUTPUT_PATH) -> None:
    output_path.parent.mkdir(parents=True, exist_ok=True)
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(records, f, indent=2, ensure_ascii=False)


def main() -> None:
    print("Ingesting documents...")
    records = ingest_documents()
    save_records(records)

    from collections import Counter
    counts = Counter(r["metadata"]["source"] for r in records)
    print(f"Done. {len(records)} records written to {OUTPUT_PATH}")
    for source, count in sorted(counts.items()):
        print(f"  {source}: {count}")


if __name__ == "__main__":
    main()
