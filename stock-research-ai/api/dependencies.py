from collections.abc import Generator

from psycopg2.extensions import connection

from database.postgres import get_db
from services.report_service import ReportService
from services.research_service import ResearchService
from services.watchlist_service import WatchlistService


def get_database() -> Generator[connection, None, None]:
    yield from get_db()


def get_research_service() -> ResearchService:
    return ResearchService()


def get_report_service() -> ReportService:
    return ReportService()


def get_watchlist_service() -> WatchlistService:
    return WatchlistService()

