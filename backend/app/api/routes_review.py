from datetime import UTC, datetime
import json

from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy import func, select
from sqlalchemy.orm import Session, joinedload

from app.api.auth import PilotContext, get_pilot_context
from app.api.routes_alerts import serialize_alert
from app.database import get_db
from app.models import Alert

router = APIRouter(prefix="/review", tags=["review"])
VALID_REVIEW_STATUSES = {"unreviewed", "confirmed", "dismissed", "needs_followup"}


class ReviewUpdate(BaseModel):
    review_status: str
    review_notes: str = ""
    assigned_to: str = ""


@router.get("/queue")
def review_queue(db: Session = Depends(get_db)) -> dict[str, object]:
    alerts = list(
        db.scalars(
            select(Alert)
            .options(joinedload(Alert.reading), joinedload(Alert.run))
            .where(Alert.review_status == "unreviewed")
            .order_by(Alert.timestamp.desc(), Alert.id.desc())
            .limit(50)
        )
    )
    total_unreviewed = db.scalar(
        select(func.count()).select_from(Alert).where(Alert.review_status == "unreviewed")
    )

    return {
        "items": [serialize_alert(alert) for alert in alerts],
        "count": total_unreviewed or 0,
    }


@router.patch("/{alert_id}")
def update_review(
    alert_id: int,
    payload: ReviewUpdate,
    context: PilotContext = Depends(get_pilot_context),
    db: Session = Depends(get_db),
) -> dict[str, object]:
    if payload.review_status not in VALID_REVIEW_STATUSES:
        raise HTTPException(status_code=422, detail="Unsupported review status")

    alert = db.scalar(
        select(Alert)
        .options(joinedload(Alert.reading), joinedload(Alert.run))
        .where(Alert.id == alert_id)
    )
    if alert is None:
        raise HTTPException(status_code=404, detail="Alert not found")

    reviewed_at = (
        None if payload.review_status == "unreviewed" else datetime.now(UTC).replace(microsecond=0)
    )
    try:
        review_history = json.loads(alert.review_history or "[]")
    except json.JSONDecodeError:
        review_history = []
    review_history.append(
        {
            "timestamp": datetime.now(UTC).replace(microsecond=0).isoformat(),
            "actor": context.actor,
            "role": context.role,
            "from_status": alert.review_status,
            "to_status": payload.review_status,
            "assigned_to": payload.assigned_to,
            "notes": payload.review_notes,
        }
    )

    alert.review_status = payload.review_status
    alert.review_notes = payload.review_notes
    alert.assigned_to = payload.assigned_to
    alert.reviewed_by = "" if payload.review_status == "unreviewed" else context.actor
    alert.review_history = json.dumps(review_history)
    alert.reviewed_at = reviewed_at
    db.commit()
    updated_alert = db.scalar(
        select(Alert)
        .options(joinedload(Alert.reading), joinedload(Alert.run))
        .where(Alert.id == alert_id)
    )

    return {"alert": serialize_alert(updated_alert)}
