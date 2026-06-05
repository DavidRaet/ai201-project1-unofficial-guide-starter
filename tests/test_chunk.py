import json
import pytest
from collections import defaultdict
from pathlib import Path

from src.chunk import chunk_all, count_tokens
from src.config import CHUNK_SIZE, OUTPUT_PATH


@pytest.fixture(scope="module")
def records():
    with open(OUTPUT_PATH, encoding="utf-8") as f:
        return json.load(f)


@pytest.fixture(scope="module")
def chunks(records):
    return chunk_all(records)


def test_no_chunk_exceeds_token_limit(chunks):
    over = [c for c in chunks if count_tokens(c["text"]) > CHUNK_SIZE]
    assert not over, f"{len(over)} chunks exceed {CHUNK_SIZE} tokens"


def test_rmp_chunks_equal_rmp_records(records, chunks):
    rmp_records = [r for r in records if r["metadata"]["source"] == "rmp"]
    rmp_chunks = [c for c in chunks if c["metadata"]["source"] == "rmp"]
    assert len(rmp_chunks) == len(rmp_records), (
        f"Expected {len(rmp_records)} rmp chunks, got {len(rmp_chunks)}"
    )


def test_miscellany_doc_splits(records, chunks):
    misc_records = [r for r in records if r["metadata"]["source"] == "miscellany"]
    assert len(misc_records) == 1
    misc_chunks = [c for c in chunks if c["metadata"]["source"] == "miscellany"]
    assert len(misc_chunks) > 1, "Miscellany article should split into multiple chunks"


def test_chunks_inherit_all_metadata(records, chunks):
    # Build a lookup of original metadata keys per source record (by source+url combo)
    for chunk in chunks:
        meta = chunk["metadata"]
        assert "source" in meta
        assert "raw_url" in meta


def test_chunk_ids_are_unique(chunks):
    ids = [c["chunk_id"] for c in chunks]
    assert len(ids) == len(set(ids)), "Duplicate chunk_ids found"


def test_chunk_index_is_int(chunks):
    for c in chunks:
        assert isinstance(c["metadata"]["chunk_index"], int)


def test_chunk_index_sequential_per_record(records):
    # Process each record individually and verify chunk_index is 0, 1, 2 ...
    from src.chunk import chunk_record, make_splitter
    splitter = make_splitter()
    for record in records:
        produced = chunk_record(record, splitter)
        indices = [c["metadata"]["chunk_index"] for c in produced]
        assert indices == list(range(len(indices))), (
            f"chunk_index not sequential for record {record['metadata']}: {indices}"
        )


def test_total_chunks_exceed_records(records, chunks):
    assert len(chunks) > len(records), (
        f"Expected more chunks ({len(chunks)}) than records ({len(records)}) "
        "since prose docs should split"
    )


def test_no_empty_chunks(chunks):
    empty = [c for c in chunks if not c["text"].strip()]
    assert not empty, f"{len(empty)} empty chunks found"
