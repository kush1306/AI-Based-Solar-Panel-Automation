from __future__ import annotations

import math
from typing import Any, Generic, Type, TypeVar, cast

from pydantic import BaseModel
from sqlalchemy import func, inspect, select
from sqlalchemy.orm import Session

from app.core.database import Base
from app.core.exceptions import NotFoundException

ModelType = TypeVar("ModelType", bound=Base)
CreateSchemaType = TypeVar("CreateSchemaType", bound=BaseModel)
UpdateSchemaType = TypeVar("UpdateSchemaType", bound=BaseModel)


class CRUDBase(Generic[ModelType, CreateSchemaType, UpdateSchemaType]):
    def __init__(self, model: Type[ModelType], resource_name: str):
        self.model = model
        self.resource_name = resource_name
        self.pk_column = inspect(model).primary_key[0]

    def get(self, db: Session, item_id: int) -> ModelType:
        obj = db.scalar(select(self.model).where(self.pk_column == item_id))
        if not obj:
            raise NotFoundException(self.resource_name, item_id)
        return obj

    def _apply_filters(self, query, filters: dict[str, Any] | None):
        if not filters:
            return query
        for field, value in filters.items():
            if value is not None and hasattr(self.model, field):
                query = query.where(getattr(self.model, field) == value)
        return query

    def get_multi(
        self,
        db: Session,
        *,
        skip: int = 0,
        limit: int = 100,
        filters: dict[str, Any] | None = None,
        order_by=None,
    ) -> tuple[list[ModelType], int]:
        query = select(self.model)
        query = self._apply_filters(query, filters)

        count_query = select(func.count()).select_from(self.model)
        count_query = self._apply_filters(count_query, filters)
        total = db.scalar(count_query) or 0

        if order_by is not None:
            query = query.order_by(order_by)
        else:
            query = query.order_by(self.pk_column.desc())

        items = list(db.scalars(query.offset(skip).limit(limit)).all())
        return cast(tuple[list[ModelType], int], (items, total))

    def create(self, db: Session, obj_in: CreateSchemaType) -> ModelType:
        data = obj_in.model_dump(exclude_unset=True)
        db_obj = self.model(**data)
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def update(
        self, db: Session, item_id: int, obj_in: UpdateSchemaType
    ) -> ModelType:
        db_obj = self.get(db, item_id)
        update_data = obj_in.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            setattr(db_obj, field, value)
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def delete(self, db: Session, item_id: int) -> None:
        db_obj = self.get(db, item_id)
        db.delete(db_obj)
        db.commit()


def paginate(total: int, page: int, page_size: int) -> dict[str, int]:
    pages = math.ceil(total / page_size) if page_size else 0
    return {"total": total, "page": page, "page_size": page_size, "pages": pages}
