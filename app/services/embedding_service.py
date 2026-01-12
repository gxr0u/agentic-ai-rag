from openai import OpenAI
import os

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

class EmbeddingService:
    def __init__(self, model: str = "text-embedding-3-small"):
        self.model = model

    def embed(self, texts: list[str]) -> list[list[float]]:
        response = client.embeddings.create(
            model=self.model,
            input=texts
        )
        return [item.embedding for item in response.data]
