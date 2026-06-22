from google import genai
from core.config import settings

class EmbeddingProvider:
    def __init__(self):
        self._client = genai.Client(api_key=settings.gemini_api_key)
        self._model = "text-embedding-004"

    async def embed_text(self, text: str) -> list[float]:
        result = self._client.models.embed_content(
            model=self._model,
            contents=text,
        )
        return result.embeddings[0].values

    async def embed_batch(self, texts: list[str]) -> list[list[float]]:
        result = self._client.models.embed_content(
            model=self._model,
            contents=texts,
        )
        return [e.values for e in result.embeddings]