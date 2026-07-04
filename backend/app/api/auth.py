from dataclasses import dataclass

from fastapi import Header, HTTPException, status

from app.config import settings


@dataclass(frozen=True)
class PilotContext:
    organization_id: str
    organization_name: str
    actor: str
    role: str


def get_pilot_context(
    x_rigsight_api_key: str | None = Header(default=None),
    x_rigsight_actor: str | None = Header(default=None),
    x_rigsight_role: str | None = Header(default=None),
) -> PilotContext:
    if settings.pilot_api_key and x_rigsight_api_key != settings.pilot_api_key:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Valid X-RigSight-API-Key header required",
        )

    return PilotContext(
        organization_id=settings.pilot_organization_id,
        organization_name=settings.pilot_organization_name,
        actor=x_rigsight_actor or "demo-operator",
        role=x_rigsight_role or "pilot-admin",
    )
