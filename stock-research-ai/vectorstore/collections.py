from qdrant_client.models import Distance, VectorParams, PayloadSchemaType
from vectorstore.qdrant_client import get_qdrant_client
from core.constants import COLLECTION_SEC_FILINGS, COLLECTION_REPORTS
from loguru import logger

EMBEDDING_DIM = 768   # text-embedding-004 output size

async def ensure_collections() -> None:
    client = get_qdrant_client()
    existing = {c.name for c in await client.get_collections().then(lambda r: r.collections)}

    for name in (COLLECTION_SEC_FILINGS, COLLECTION_REPORTS):
        if name not in existing:
            await client.create_collection(
                collection_name=name,
                vectors_config=VectorParams(size=EMBEDDING_DIM, distance=Distance.COSINE),
            )
            logger.info(f"Created Qdrant collection: {name}")