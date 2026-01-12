# app/rag/retriever.py
from pathlib import Path

import os
import pickle
from typing import List, Dict

import faiss
import numpy as np

from app.services.embedding_service import get_embeddings

BASE_DIR = Path(__file__).resolve().parents[2]
VECTOR_STORE_PATH = BASE_DIR / "data" / "vector_store"

INDEX_FILE = "index.faiss"
META_FILE = "metadata.pkl"

index_path = VECTOR_STORE_PATH / INDEX_FILE

if not index_path.exists():
    raise RuntimeError("FAISS index not found. Run ingestion first.")


class Retriever:
    def __init__(self):
        index_path = os.path.join(VECTOR_STORE_PATH, INDEX_FILE)
        meta_path = os.path.join(VECTOR_STORE_PATH, META_FILE)

        if not os.path.exists(index_path):
            raise RuntimeError("FAISS index not found. Run ingestion first.")

        self.index = faiss.read_index(index_path)

        with open(meta_path, "rb") as f:
            self.metadata = pickle.load(f)

    def retrieve(self, query: str, top_k: int = 4) -> List[Dict]:
        query_embedding = get_embeddings([query])
        query_embedding = np.array(query_embedding).astype("float32")

        distances, indices = self.index.search(query_embedding, top_k)

        results = []
        for idx in indices[0]:
            results.append(self.metadata[idx])

        return results
