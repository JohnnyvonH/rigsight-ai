from fastapi import APIRouter

from app.api import (
    routes_alerts,
    routes_camera,
    routes_health,
    routes_readings,
    routes_review,
    routes_runs,
)

api_router = APIRouter()
api_router.include_router(routes_health.router)
api_router.include_router(routes_readings.router)
api_router.include_router(routes_alerts.router)
api_router.include_router(routes_runs.router)
api_router.include_router(routes_review.router)
api_router.include_router(routes_camera.router)
