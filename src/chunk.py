import json
import uuid
from pathlib import Path
from typing import TYPE_CHECKING

from langchain_text_splitters import RecursiveCharacterTextSplitter

from src.config import CHUNK_OVERLAP, CHUNK_SIZE, CHUNKS_PATH, OUTPUT_PATH

if TYPE_CHECKING:
    from transformers import PreTrainedTokenizerBase

_tokenizer: "PreTrainedTokenizerBase | None" = None


def get_tokenizer() -> "PreTrainedTokenizerBase":
    global _tokenizer
    if _tokenizer is None:
        from transformers import AutoTokenizer
        _tokenizer = AutoTokenizer.from_pretrained("sentence-transformers/all-MiniLM-L6-v2")
    return _tokenizer


def count_tokens(text: str) -> int:
    return len(get_tokenizer().encode(text, add_special_tokens=False))


def make_splitter() -> RecursiveCharacterTextSplitter:
    return RecursiveCharacterTextSplitter(
        chunk_size=CHUNK_SIZE,
        chunk_overlap=CHUNK_OVERLAP,
        length_function=count_tokens,
        separators=["\n\n", "\n", ". ", "! ", "? ", " ", ""],
    )


def chunk_record(record: dict, splitter: RecursiveCharacterTextSplitter) -> list[dict]:
    texts = splitter.split_text(record["text"])
    chunks = []
    for i, text in enumerate(texts):
        chunks.append({
            "chunk_id": str(uuid.uuid4()),
            "text": text,
            "metadata": {**record["metadata"], "chunk_index": i},
        })
    return chunks


def chunk_all(records: list[dict]) -> list[dict]:
    splitter = make_splitter()
    chunks = []
    for record in records:
        chunks.extend(chunk_record(record, splitter))
    return chunks


def save_chunks(chunks: list[dict], path: Path = CHUNKS_PATH) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        json.dump(chunks, f, indent=2, ensure_ascii=False)


def main() -> None:
    print("Chunking documents...")
    with open(OUTPUT_PATH, encoding="utf-8") as f:
        records = json.load(f)

    chunks = chunk_all(records)
    save_chunks(chunks)

    from collections import Counter
    counts = Counter(c["metadata"]["source"] for c in chunks)
    print(f"Done. {len(chunks)} chunks written to {CHUNKS_PATH}")
    for source, count in sorted(counts.items()):
        print(f"  {source}: {count}")


if __name__ == "__main__":
    main()