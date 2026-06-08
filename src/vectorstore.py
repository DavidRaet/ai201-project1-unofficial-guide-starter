import json
from pathlib import Path
from typing import TYPE_CHECKING

import chromadb

from src.config import CHROMA_DIR, CHUNKS_PATH, COLLECTION_NAME, TOP_K

if TYPE_CHECKING:
    from sentence_transformers import SentenceTransformer as _ST

_model: "_ST | None" = None


def get_model() -> "_ST":
    global _model
    if _model is None:
        from sentence_transformers import SentenceTransformer
        _model = SentenceTransformer("all-MiniLM-L6-v2")
    return _model


def embed_texts(texts: list[str]) -> list[list[float]]:
    return get_model().encode(texts, batch_size=32, show_progress_bar=False).tolist()


def make_persistent_client(chroma_dir: Path = CHROMA_DIR) -> chromadb.PersistentClient:
    chroma_dir.mkdir(parents=True, exist_ok=True)
    return chromadb.PersistentClient(path=str(chroma_dir))


def make_collection(
    client: chromadb.Client,
    name: str = COLLECTION_NAME,
    reset: bool = False,
) -> chromadb.Collection:
    if reset:
        try:
            client.delete_collection(name)
        except Exception:
            pass
        return client.create_collection(
            name=name,
            metadata={"hnsw:space": "cosine"},
        )
    return client.get_or_create_collection(
        name=name,
        metadata={"hnsw:space": "cosine"},
    )


def build_vector_store(chunks: list[dict], collection: chromadb.Collection) -> None:
    ids = [c["chunk_id"] for c in chunks]
    texts = [c["text"] for c in chunks]
    metadatas = [c["metadata"] for c in chunks]
    embeddings = embed_texts(texts)
    collection.add(ids=ids, documents=texts, embeddings=embeddings, metadatas=metadatas)


def retrieve(
    query: str,
    collection: chromadb.Collection,
    k: int = TOP_K,
) -> list[dict]:
    embedding = embed_texts([query])[0]
    results = collection.query(query_embeddings=[embedding], n_results=k)
    return [
        {
            "chunk_id": results["ids"][0][i],
            "text":     results["documents"][0][i],
            "metadata": results["metadatas"][0][i],
            "distance": results["distances"][0][i],
        }
        for i in range(len(results["ids"][0]))
    ]


def main() -> None:
    print("Building vector store...")
    with open(CHUNKS_PATH, encoding="utf-8") as f:
        chunks = json.load(f)

    client = make_persistent_client()
    collection = make_collection(client, reset=True)
    build_vector_store(chunks, collection)
    print(f"Done. {collection.count()} chunks embedded into '{COLLECTION_NAME}'.")

    print("\nSmoke test — 'Are Professor Anna's lectures for CMPU145 well-received by students?'")
    results = retrieve("Are Professor Anna's lectures for CMPU145 well-received by students?", collection, k=5)
    for i, r in enumerate(results, 1):
        src = r["metadata"].get("professor_name", r["metadata"].get("source", ""))
        print(f"  [{i}] (dist={r['distance']:.4f}) [{src}] {r['text'][:80]}...")


if __name__ == "__main__":
    main()
