from fastapi import APIRouter

from app.api import (
    routes_alerts,
    routes_camera,
    routes_demo,
    routes_health,
    routes_readings,
    routes_reports,
    routes_review,
    routes_runs,
)

api_router = APIRouter()
versioned_router = APIRouter(prefix="/api/v1")

for router in (
    routes_health.router,
    routes_readings.router,
    routes_alerts.router,
    routes_runs.router,
    routes_review.router,
    routes_camera.router,
    routes_demo.router,
    routes_reports.router,
):
    api_router.include_router(router)
    versioned_router.include_router(router)

api_router.include_router(versioned_router)
