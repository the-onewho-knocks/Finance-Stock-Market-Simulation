from llama_index.embeddings.gemini import GeminiEmbedding
from core.config import settings
from loguru import logger

class EmbeddingProvider:
    def __init__(self):
        self._model = GeminiEmbedding(
            model_name="models/text-embedding-004",
            api_key=settings.gemini_api_key,
        )

    async def embed_text(self, text: str) -> list[float]:
        return await self._model.aget_text_embedding(text)

    async def embed_batch(self, texts: list[str]) -> list[list[float]]:
        return await self._model.aget_text_embedding_batch(texts)