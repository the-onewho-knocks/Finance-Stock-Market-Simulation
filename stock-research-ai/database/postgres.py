from collections.abc import Generator

import psycopg2
from psycopg2.extras import RealDictCursor

from core.config import settings


def get_connection():
    return psycopg2.connect(
        settings.database_url,
        cursor_factory=RealDictCursor,
    )


def get_db() -> Generator:
    conn = get_connection()
    try:
        yield conn
    finally:
        conn.close()


def init_db() -> None:
    conn = get_connection()
    try:
        with conn.cursor() as cur:
            cur.execute(
                """
                CREATE TABLE IF NOT EXISTS research_runs (
                    id TEXT PRIMARY KEY,
                    symbol TEXT NOT NULL,
                    user_id TEXT,
                    input_payload JSONB NOT NULL,
                    final_response JSONB,
                    agent_outputs JSONB,
                    errors JSONB,
                    status TEXT NOT NULL DEFAULT 'running',
                    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
                    completed_at TIMESTAMP
                );
                CREATE INDEX IF NOT EXISTS idx_research_runs_symbol
                    ON research_runs(symbol);
                CREATE INDEX IF NOT EXISTS idx_research_runs_user_id
                    ON research_runs(user_id);
                """
            )
        conn.commit()
    finally:
        conn.close()