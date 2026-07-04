from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from app.crud import alert_crud
from app.core.database import get_db
from app.schemas.common import MessageResponse, PaginatedResponse
from app.schemas.entities import AlertCreate, AlertResponse, AlertUpdate
from app.utils.pagination import paginate_meta, pagination_params

router = APIRouter(prefix="/alerts", tags=["Alerts"])


@router.get("", response_model=PaginatedResponse[AlertResponse])
async def list_alerts(
    db: Session = Depends(get_db),
    pagination: dict = Depends(pagination_params),
    search: str | None = Query(None),
    status: str | None = Query(None),
    severity: str | None = Query(None),
    sort_by: str = Query("alert_id"),
    sort_order: str = Query("desc", pattern="^(asc|desc)$"),
):
    filters = {k: v for k, v in {"status": status, "severity": severity}.items() if v}
    items, total = alert_crud.get_multi(
        db,
        skip=pagination["skip"],
        limit=pagination["limit"],
        filters=filters or None,
        search=search,
        search_fields=["alert_type", "message"],
        sort_by=sort_by,
        sort_order=sort_order,
    )
    meta = paginate_meta(total, pagination["page"], pagination["page_size"])
    return PaginatedResponse[AlertResponse](
        items=[AlertResponse.model_validate(i) for i in items],
        **meta,
    )


@router.get("/active", response_model=list[AlertResponse])
async def list_active_alerts(db: Session = Depends(get_db)):
    items, _ = alert_crud.get_multi(db, skip=0, limit=100, filters={"status": "Active"})
    return [AlertResponse.model_validate(i) for i in items]


@router.get("/history", response_model=PaginatedResponse[AlertResponse])
async def list_alert_history(
    db: Session = Depends(get_db),
    pagination: dict = Depends(pagination_params),
):
    items, total = alert_crud.get_multi(
        db,
        skip=pagination["skip"],
        limit=pagination["limit"],
        filters={"status": "Resolved"},
    )
    meta = paginate_meta(total, pagination["page"], pagination["page_size"])
    return PaginatedResponse[AlertResponse](
        items=[AlertResponse.model_validate(i) for i in items],
        **meta,
    )


@router.get("/{item_id}", response_model=AlertResponse)
async def get_alert(item_id: int, db: Session = Depends(get_db)):
    item = alert_crud.get(db, item_id)
    return AlertResponse.model_validate(item)


@router.post("", response_model=AlertResponse, status_code=201)
async def create_alert(payload: AlertCreate, db: Session = Depends(get_db)):
    item = alert_crud.create(db, payload)
    return AlertResponse.model_validate(item)


@router.put("/{item_id}", response_model=AlertResponse)
async def update_alert(item_id: int, payload: AlertUpdate, db: Session = Depends(get_db)):
    item = alert_crud.update(db, item_id, payload)
    return AlertResponse.model_validate(item)


@router.delete("/{item_id}", response_model=MessageResponse)
async def delete_alert(item_id: int, db: Session = Depends(get_db)):
    alert_crud.delete(db, item_id)
    return MessageResponse(message="Alert deleted successfully")
