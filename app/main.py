# app/main.py

from fastapi import FastAPI
from app.api.routes import router

app = FastAPI(
    title="AI Agent RAG System",
    description="Agentic AI system with RAG and tool calling",
    version="1.0.0"
)

app.include_router(router)


@app.get("/")
def health_check():
    return {"status": "ok"}
