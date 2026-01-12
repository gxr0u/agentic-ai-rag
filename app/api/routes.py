# app/api/routes.py

from fastapi import APIRouter, HTTPException
from app.agent.controller import run_agent
from app.models.schemas import AskRequest, AskResponse

router = APIRouter()


@router.post("/ask", response_model=AskResponse)
def ask_question(payload: AskRequest):
    try:
        result = run_agent(
            query=payload.query,
            session_id=payload.session_id
        )

        return AskResponse(
            answer=result["answer"],
            source=result["sources"],
            session_id=result["session_id"]
        )

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
