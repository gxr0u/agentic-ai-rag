# app/agent/controller.py

from typing import Dict, Any
import uuid

import openai

from app.agent.prompts import SYSTEM_PROMPT, DECISION_PROMPT
from app.agent.tools import retrieve_documents
from app.agent.memory import SessionMemory
from app.config.settings import OPENAI_MODEL

memory = SessionMemory()


def _llm_call(messages):
    response = openai.chat.completions.create(
        model=OPENAI_MODEL,
        messages=messages,
        temperature=0
    )
    return response.choices[0].message.content.strip()


def decide_action(query: str) -> str:
    """
    Uses LLM to decide whether retrieval is needed.
    """
    decision = _llm_call([
        {"role": "system", "content": DECISION_PROMPT.format(query=query)}
    ])
    return decision


def run_agent(query: str, session_id: str | None = None) -> Dict[str, Any]:
    """
    Main agent execution function.
    """
    if session_id is None:
        session_id = str(uuid.uuid4())

    # Retrieve memory
    history = memory.get(session_id)

    # Step 1: Decide action
    action = decide_action(query)

    sources = []
    context = ""

    # Step 2: Tool calling if needed
    if action == "RETRIEVE":
        docs = retrieve_documents(query)
        context = "\n\n".join(d["text"] for d in docs)
        sources = list({d["source"] for d in docs})

    # Step 3: Build final prompt
    messages = [
        {"role": "system", "content": SYSTEM_PROMPT}
    ]

    messages.extend(history)

    if context:
        messages.append({
            "role": "system",
            "content": f"Relevant documents:\n{context}"
        })

    messages.append({"role": "user", "content": query})

    answer = _llm_call(messages)

    # Step 4: Update memory
    memory.add(session_id, "user", query)
    memory.add(session_id, "assistant", answer)

    return {
        "answer": answer,
        "sources": sources,
        "session_id": session_id
    }
