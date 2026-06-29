from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.schemas.common import MessageResponse, PaginatedResponse
from app.schemas.entities import SystemLogCreate, SystemLogResponse
from app.services.base import paginate
from app.services.crud import system_log_service
from app.utils.pagination import pagination_params

router = APIRouter(prefix="/logs", tags=["System Logs"])


@router.get("", response_model=PaginatedResponse[SystemLogResponse])
async def list_logs(
    db: Session = Depends(get_db),
    pagination: dict = Depends(pagination_params),
    search: str | None = Query(None),
    status: str | None = Query(None),
    module: str | None = Query(None),
):
    filters: dict[str, str] = {}
    if status:
        filters["status"] = status
    if module:
        filters["module"] = module

    items, total = system_log_service.get_multi(
        db,
        skip=pagination["skip"],
        limit=pagination["limit"],
        filters=filters or None,
    )
    if search:
        lowered = search.lower()
        items = [
            log
            for log in items
            if lowered in (log.description or "").lower()
            or lowered in (log.event_type or "").lower()
        ]
        total = len(items)
    meta = paginate(total, pagination["page"], pagination["page_size"])
    return PaginatedResponse[SystemLogResponse](
        items=[SystemLogResponse.model_validate(i) for i in items],
        **meta,
    )


@router.get("/{item_id}", response_model=SystemLogResponse)
async def get_log(item_id: int, db: Session = Depends(get_db)):
    item = system_log_service.get(db, item_id)
    return SystemLogResponse.model_validate(item)


@router.post("", response_model=SystemLogResponse, status_code=201)
async def create_log(payload: SystemLogCreate, db: Session = Depends(get_db)):
    item = system_log_service.create(db, payload)
    return SystemLogResponse.model_validate(item)


@router.delete("/{item_id}", response_model=MessageResponse)
async def delete_log(item_id: int, db: Session = Depends(get_db)):
    system_log_service.delete(db, item_id)
    return MessageResponse(message="System log deleted successfully")
