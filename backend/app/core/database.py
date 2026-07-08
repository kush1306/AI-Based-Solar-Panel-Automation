from collections.abc import Generator
import logging

from functools import lru_cache

from sqlalchemy import create_engine, inspect
from sqlalchemy.orm import DeclarativeBase, Session, sessionmaker

from app.core.config import settings

logger = logging.getLogger(__name__)


class Base(DeclarativeBase):
    pass


@lru_cache
def get_engine():
    return create_engine(
        settings.sqlalchemy_database_url,
        pool_pre_ping=True,
        pool_recycle=3600,
        echo=settings.debug,
        connect_args={"charset": "utf8mb4"},
    )


SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=get_engine())


def get_db() -> Generator[Session, None, None]:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def init_database() -> None:
    """
    Ensure all SQLAlchemy model tables exist in the connected database.

    Uses Base.metadata.create_all(), which only creates missing tables and
    never drops or modifies existing tables or data.
    """
    import app.models  # noqa: F401 — register all ORM models on Base.metadata

    engine = get_engine()
    existing_tables = set(inspect(engine).get_table_names())
    expected_tables = set(Base.metadata.tables.keys())
    missing_tables = sorted(expected_tables - existing_tables)

    Base.metadata.create_all(bind=engine)

    if missing_tables:
        logger.info("Created missing database tables: %s", ", ".join(missing_tables))
    else:
        logger.info("Database schema check complete; all model tables already exist.")
