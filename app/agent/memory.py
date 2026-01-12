# app/agent/memory.py

from typing import List, Dict
from collections import defaultdict

class SessionMemory:
    def __init__(self, max_turns: int = 5):
        self.store = defaultdict(list)
        self.max_turns = max_turns

    def get(self, session_id: str) -> List[Dict]:
        return self.store.get(session_id, [])

    def add(self, session_id: str, role: str, content: str):
        self.store[session_id].append({
            "role": role,
            "content": content
        })

        # keep memory bounded
        if len(self.store[session_id]) > self.max_turns * 2:
            self.store[session_id] = self.store[session_id][-self.max_turns * 2:]
