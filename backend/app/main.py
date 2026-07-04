from collections.abc import AsyncIterator
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.router import api_router
from app.config import settings
from app.database import Base, SessionLocal, engine, run_sqlite_compat_migrations
from app.services.demo_data import ensure_demo_data


@asynccontextmanager
async def lifespan(_: FastAPI) -> AsyncIterator[None]:
    Base.metadata.create_all(bind=engine)
    run_sqlite_compat_migrations()
    with SessionLocal() as db:
        ensure_demo_data(db)
    yield


def create_app() -> FastAPI:
    app = FastAPI(
        title="RigSight AI API",
        description="Synthetic telemetry and anomaly-monitoring API for RigSight AI.",
        version=settings.app_version,
        lifespan=lifespan,
    )

    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.cors_origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    app.include_router(api_router)
    return app


app = create_app()
