from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.schemas.common import MessageResponse, PaginatedResponse
from app.schemas.entities import AlertCreate, AlertResponse, AlertUpdate
from app.services.base import paginate
from app.services.crud import alert_service
from app.utils.pagination import pagination_params

router = APIRouter(prefix="/alerts", tags=["Alerts"])


@router.get("", response_model=PaginatedResponse[AlertResponse])
async def list_alerts(
    db: Session = Depends(get_db),
    pagination: dict = Depends(pagination_params),
    search: str | None = Query(None),
    status: str | None = Query(None),
    severity: str | None = Query(None),
):
    filters = {"status": status, "severity": severity}
    items, total = alert_service.get_multi(
        db,
        skip=pagination["skip"],
        limit=pagination["limit"],
        filters={k: v for k, v in filters.items() if v},
    )
    if search:
        lowered = search.lower()
        items = [
            a
            for a in items
            if lowered in (a.alert_type or "").lower() or lowered in (a.message or "").lower()
        ]
        total = len(items)
    meta = paginate(total, pagination["page"], pagination["page_size"])
    return PaginatedResponse[AlertResponse](
        items=[AlertResponse.model_validate(i) for i in items],
        **meta,
    )


@router.get("/active", response_model=list[AlertResponse])
async def list_active_alerts(db: Session = Depends(get_db)):
    items, _ = alert_service.get_multi(db, skip=0, limit=100, filters={"status": "Active"})
    return [AlertResponse.model_validate(i) for i in items]


@router.get("/history", response_model=PaginatedResponse[AlertResponse])
async def list_alert_history(
    db: Session = Depends(get_db),
    pagination: dict = Depends(pagination_params),
):
    items, total = alert_service.get_multi(
        db,
        skip=pagination["skip"],
        limit=pagination["limit"],
        filters={"status": "Resolved"},
    )
    meta = paginate(total, pagination["page"], pagination["page_size"])
    return PaginatedResponse[AlertResponse](
        items=[AlertResponse.model_validate(i) for i in items],
        **meta,
    )


@router.get("/{item_id}", response_model=AlertResponse)
async def get_alert(item_id: int, db: Session = Depends(get_db)):
    item = alert_service.get(db, item_id)
    return AlertResponse.model_validate(item)


@router.post("", response_model=AlertResponse, status_code=201)
async def create_alert(payload: AlertCreate, db: Session = Depends(get_db)):
    item = alert_service.create(db, payload)
    return AlertResponse.model_validate(item)


@router.put("/{item_id}", response_model=AlertResponse)
async def update_alert(item_id: int, payload: AlertUpdate, db: Session = Depends(get_db)):
    item = alert_service.update(db, item_id, payload)
    return AlertResponse.model_validate(item)


@router.delete("/{item_id}", response_model=MessageResponse)
async def delete_alert(item_id: int, db: Session = Depends(get_db)):
    alert_service.delete(db, item_id)
    return MessageResponse(message="Alert deleted successfully")
