from collections.abc import Generator

from sqlalchemy import create_engine, text
from sqlalchemy.orm import DeclarativeBase, Session, sessionmaker

from app.config import settings


class Base(DeclarativeBase):
    pass


connect_args = {"check_same_thread": False} if settings.database_url.startswith("sqlite") else {}

engine = create_engine(settings.database_url, connect_args=connect_args)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, expire_on_commit=False, bind=engine)


SQLITE_COMPAT_COLUMNS = {
    "test_runs": {
        "organization_id": "TEXT NOT NULL DEFAULT 'demo-org'",
        "rig_id": "TEXT NOT NULL DEFAULT 'synthetic-rig-01'",
    },
    "readings": {
        "organization_id": "TEXT NOT NULL DEFAULT 'demo-org'",
        "rig_id": "TEXT NOT NULL DEFAULT 'synthetic-rig-01'",
        "source": "TEXT NOT NULL DEFAULT 'synthetic'",
    },
    "alerts": {
        "organization_id": "TEXT NOT NULL DEFAULT 'demo-org'",
        "rig_id": "TEXT NOT NULL DEFAULT 'synthetic-rig-01'",
        "assigned_to": "TEXT NOT NULL DEFAULT ''",
        "reviewed_by": "TEXT NOT NULL DEFAULT ''",
        "review_history": "TEXT NOT NULL DEFAULT '[]'",
    },
}


def run_sqlite_compat_migrations() -> None:
    """Keep existing local demo databases compatible until Alembic is introduced."""
    if not settings.database_url.startswith("sqlite"):
        return

    with engine.begin() as connection:
        for table_name, columns in SQLITE_COMPAT_COLUMNS.items():
            existing = {
                row[1]
                for row in connection.execute(text(f"PRAGMA table_info({table_name})")).fetchall()
            }
            for column_name, ddl in columns.items():
                if column_name not in existing:
                    connection.execute(text(f"ALTER TABLE {table_name} ADD COLUMN {column_name} {ddl}"))


def get_db() -> Generator[Session, None, None]:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
