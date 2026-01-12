# app/rag/ingest.py
from pathlib import Path

import os
import pickle
from typing import List, Dict

import faiss
import numpy as np

from app.rag.chunking import chunk_text
from app.services.embedding_service import get_embeddings


BASE_DIR = Path(__file__).resolve().parents[2]
VECTOR_STORE_PATH = BASE_DIR / "data" / "vector_store"

INDEX_FILE = "index.faiss"
META_FILE = "metadata.pkl"


def load_documents(doc_dir: str) -> List[Dict]:
    documents = []

    for filename in os.listdir(doc_dir):
        if not filename.endswith(".txt"):
            continue

        path = os.path.join(doc_dir, filename)
        with open(path, "r", encoding="utf-8") as f:
            text = f.read()

        documents.append({
            "source": filename,
            "text": text
        })

    return documents


def ingest_documents(doc_dir: str):
    os.makedirs(VECTOR_STORE_PATH, exist_ok=True)

    docs = load_documents(doc_dir)

    all_chunks = []
    metadata = []

    for doc in docs:
        chunks = chunk_text(doc["text"])
        for chunk in chunks:
            all_chunks.append(chunk)
            metadata.append({
                "source": doc["source"],
                "text": chunk
            })

    print(f"[INGEST] Total chunks: {len(all_chunks)}")

    embeddings = get_embeddings(all_chunks)
    embeddings = np.array(embeddings).astype("float32")

    dim = embeddings.shape[1]
    index = faiss.IndexFlatL2(dim)
    index.add(embeddings)

    faiss.write_index(index, str(VECTOR_STORE_PATH / INDEX_FILE))

    with open(VECTOR_STORE_PATH / META_FILE, "wb") as f:
        pickle.dump(metadata, f)


    print("[INGEST] Vector store created successfully")


if __name__ == "__main__":
    ingest_documents("data/raw_docs")
