from typing import Type, TypeVar, Generic
from sqlalchemy.orm import Session
from sqlalchemy import insert
from infrastructure.sqlite.database import Base

ModelType = TypeVar('ModelType', bound=Base)


class BaseRepository(Generic[ModelType]):
    def __init__(self, model: Type[ModelType], not_found_exception: Type[Exception]):
        self._model = model
        self._not_found_exception = not_found_exception

    def create(self, session: Session, **data) -> ModelType:
        query = insert(self._model).values(**data).returning(self._model)
        obj = session.scalar(query)
        return obj

    def get_by_id(self, session: Session, id: int) -> ModelType:
        obj = session.query(self._model).get(id)
        if obj is None:
            raise self._not_found_exception(id)
        return obj

    def get_all(
            self, session: Session, limit: int = 100, offset: int = 0
    ) -> list[ModelType]:
        query = session.query(self._model).limit(limit).offset(offset).all()
        return query

    def update(self, session: Session, id: int, **data) -> ModelType:
        obj = self.get_by_id(session, id)
        if obj is None:
            raise self._not_found_exception(id)
        for key, value in data.items():
            if hasattr(obj, key):
                setattr(obj, key, value)
        return obj

    def delete(self, session: Session, id: int) -> bool:
        obj = self.get_by_id(session, id)
        session.delete(obj)