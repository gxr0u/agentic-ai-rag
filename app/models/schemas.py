# app/models/schemas.py

from pydantic import BaseModel
from typing import Optional, List


class AskRequest(BaseModel):
    query: str
    session_id: Optional[str] = None


class AskResponse(BaseModel):
    answer: str
    source: List[str]
    session_id: str
