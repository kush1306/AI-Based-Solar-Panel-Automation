from __future__ import annotations

from typing import Any, Generic, Type, TypeVar, cast

from pydantic import BaseModel
from sqlalchemy import String, cast as sql_cast, func, inspect as sa_inspect, or_, select
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
        self.pk_column = sa_inspect(model).primary_key[0]
        self.pk_name = self.pk_column.key

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

    def _apply_search(self, query, search: str | None, search_fields: list[str] | None):
        if not search or not search_fields:
            return query
        term = f"%{search}%"
        clauses = []
        for field in search_fields:
            if hasattr(self.model, field):
                column = getattr(self.model, field)
                clauses.append(sql_cast(column, String).like(term))
        if clauses:
            query = query.where(or_(*clauses))
        return query

    def _resolve_sort_column(self, sort_by: str | None):
        if sort_by and hasattr(self.model, sort_by):
            return getattr(self.model, sort_by)
        return self.pk_column

    def get_multi(
        self,
        db: Session,
        *,
        skip: int = 0,
        limit: int = 100,
        filters: dict[str, Any] | None = None,
        search: str | None = None,
        search_fields: list[str] | None = None,
        sort_by: str | None = None,
        sort_order: str = "desc",
    ) -> tuple[list[ModelType], int]:
        query = select(self.model)
        query = self._apply_filters(query, filters)
        query = self._apply_search(query, search, search_fields)

        count_query = select(func.count()).select_from(self.model)
        count_query = self._apply_filters(count_query, filters)
        count_query = self._apply_search(count_query, search, search_fields)
        total = db.scalar(count_query) or 0

        sort_column = self._resolve_sort_column(sort_by)
        ordering = sort_column.asc() if sort_order == "asc" else sort_column.desc()
        query = query.order_by(ordering)

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
