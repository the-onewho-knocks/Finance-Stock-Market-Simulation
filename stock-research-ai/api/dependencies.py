from fastapi import Depends
from psycopg2.extensions import connection

from database.postgres import get_db
from services.research_service import ResearchService


def get_database() -> connection:
    for conn in get_db():
        return conn


def get_research_service() -> ResearchService:
    return ResearchService()