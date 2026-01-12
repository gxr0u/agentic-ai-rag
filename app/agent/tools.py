# app/agent/tools.py

from typing import List, Dict
from app.rag.retriever import Retriever

retriever = Retriever()


def retrieve_documents(query: str, top_k: int = 4) -> List[Dict]:
    """
    Tool: Retrieves relevant document chunks for a given query.
    """
    results = retriever.retrieve(query, top_k=top_k)
    return results
