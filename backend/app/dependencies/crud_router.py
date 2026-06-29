from __future__ import annotations

from typing import Any, Callable, Sequence, Type, cast

from fastapi import APIRouter, Body, Depends, Query
from pydantic import BaseModel
from sqlalchemy.orm import Session

from app.crud.base import CRUDBase
from app.core.database import get_db
from app.schemas.common import MessageResponse, PaginatedResponse
from app.utils.pagination import paginate_meta, pagination_params


def create_crud_router(
    *,
    prefix: str,
    tags: Sequence[str],
    crud: CRUDBase[Any, Any, Any],
    response_schema: Type[BaseModel],
    create_schema: Type[BaseModel],
    update_schema: Type[BaseModel],
    resource_label: str,
    search_fields: list[str] | None = None,
    filter_params: Callable[[], dict[str, Any]] | None = None,
) -> APIRouter:
    router = APIRouter(prefix=prefix, tags=list(tags))
    paginated_model = cast(
        type[PaginatedResponse[Any]],
        PaginatedResponse[response_schema],  # type: ignore[valid-type]
    )
    default_sort = crud.pk_name
    create_body_schema = create_schema.model_json_schema()
    update_body_schema = update_schema.model_json_schema()

    @router.get("", response_model=paginated_model)
    async def list_items(
        db: Session = Depends(get_db),
        pagination: dict = Depends(pagination_params),
        search: str | None = Query(None, description="Search filter"),
        sort_by: str = Query(default_sort, description="Sort field"),
        sort_order: str = Query("desc", pattern="^(asc|desc)$"),
    ):
        filters: dict[str, Any] = {}
        if filter_params:
            filters.update(filter_params())

        items, total = crud.get_multi(
            db,
            skip=pagination["skip"],
            limit=pagination["limit"],
            filters=filters or None,
            search=search,
            search_fields=search_fields,
            sort_by=sort_by,
            sort_order=sort_order,
        )

        meta = paginate_meta(total, pagination["page"], pagination["page_size"])
        return paginated_model(
            items=[response_schema.model_validate(item) for item in items],
            **meta,
        )

    @router.get("/{item_id}", response_model=response_schema)
    async def get_item(item_id: int, db: Session = Depends(get_db)):
        item = crud.get(db, item_id)
        return response_schema.model_validate(item)

    @router.post("", response_model=response_schema, status_code=201)
    async def create_item(
        payload: dict[str, Any] = Body(..., json_schema_extra=create_body_schema),
        db: Session = Depends(get_db),
    ):
        validated = create_schema.model_validate(payload)
        item = crud.create(db, validated)
        return response_schema.model_validate(item)

    @router.put("/{item_id}", response_model=response_schema)
    async def update_item(
        item_id: int,
        payload: dict[str, Any] = Body(..., json_schema_extra=update_body_schema),
        db: Session = Depends(get_db),
    ):
        validated = update_schema.model_validate(payload)
        item = crud.update(db, item_id, validated)
        return response_schema.model_validate(item)

    @router.delete("/{item_id}", response_model=MessageResponse)
    async def delete_item(item_id: int, db: Session = Depends(get_db)):
        crud.delete(db, item_id)
        return MessageResponse(message=f"{resource_label} deleted successfully")

    return router
