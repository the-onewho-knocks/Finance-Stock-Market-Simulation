from fastapi import FastAPI

from api.v1.health import router as health_router
from api.v1.research import router as research_router
from core.config import settings
from core.logging import configure_logging
from database.postgres import init_db

configure_logging(settings.debug)

try:
    init_db()
except Exception:
    pass

app = FastAPI(
    title="Stock Research AI",
    version="0.1.0",
    debug=settings.debug,
)

app.include_router(health_router)
app.include_router(research_router)


@app.get("/")
async def root() -> dict[str, str]:
    return {
        "service": "stock-research-ai",
        "status": "ok",
    }