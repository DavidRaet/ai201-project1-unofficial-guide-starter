import json
import pytest
import chromadb

from src.config import CHUNKS_PATH, COLLECTION_NAME, TOP_K
from src.vectorstore import build_vector_store, embed_texts, make_collection, retrieve


@pytest.fixture(scope="module")
def chunks():
    with open(CHUNKS_PATH, encoding="utf-8") as f:
        return json.load(f)


@pytest.fixture(scope="module")
def populated_collection(chunks):
    client = chromadb.EphemeralClient()
    col = make_collection(client, name=COLLECTION_NAME, reset=True)
    build_vector_store(chunks, col)
    return col


# ── Embedding ─────────────────────────────────────────────────────────────────

def test_embed_single_returns_correct_dim():
    vectors = embed_texts(["hello world"])
    assert len(vectors) == 1
    assert len(vectors[0]) == 384  # all-MiniLM-L6-v2 output dimension


def test_embed_batch_length_matches():
    texts = ["alpha", "beta", "gamma"]
    vectors = embed_texts(texts)
    assert len(vectors) == 3
    assert all(len(v) == 384 for v in vectors)


# ── Collection population ─────────────────────────────────────────────────────

def test_collection_count_matches_chunks(populated_collection, chunks):
    assert populated_collection.count() == len(chunks)


# ── Retrieval shape ───────────────────────────────────────────────────────────

def test_retrieve_returns_k_results(populated_collection):
    results = retrieve("Jacob Erickson", populated_collection)
    assert len(results) == TOP_K


def test_retrieve_result_has_required_keys(populated_collection):
    results = retrieve("Jacob Erickson", populated_collection)
    for r in results:
        assert "chunk_id" in r
        assert "text" in r
        assert "metadata" in r
        assert "distance" in r


def test_retrieve_distance_ascending(populated_collection):
    results = retrieve("Jacob Erickson", populated_collection)
    distances = [r["distance"] for r in results]
    assert distances == sorted(distances), "Results not sorted by ascending distance"


def test_retrieve_k_override(populated_collection):
    results = retrieve("workload", populated_collection, k=3)
    assert len(results) == 3


# ── Retrieval relevance ───────────────────────────────────────────────────────

def test_retrieve_relevance_erickson(populated_collection):
    results = retrieve("Jacob Erickson grading homework", populated_collection)
    top = results[0]
    assert top["metadata"].get("professor_name") == "Jacob Erickson", (
        f"Expected Jacob Erickson in top result, got: {top['metadata']}"
    )


def test_retrieve_relevance_gordon(populated_collection):
    # CMPU-240 reviews are very short and generic, so we check top-5 rather than top-1
    results = retrieve("Jonathan Gordon CMPU-240", populated_collection)
    hit = any(
        r["metadata"].get("course_code") == "CMPU-240"
        or r["metadata"].get("professor_name") == "Jonathan Gordon"
        for r in results
    )
    assert hit, f"No CMPU-240 / Gordon result in top-5: {[r['metadata'] for r in results]}"
