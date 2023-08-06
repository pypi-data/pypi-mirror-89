# -*- coding: utf-8 -*-
"""
    fiber.crud.base
    ~~~~~~~~~~

    Crud base utilities

    :copyright: (c) 2020 by Robin Raymond.
    :license: MIT, see LICENSE for more details.
"""
# pylint: disable=no-name-in-module
# pylint: disable=no-self-argument
from typing import Generic, List, Type, TypeVar
from uuid import UUID

from pydantic import BaseModel
from sqlalchemy.orm import Session

from fiber.models.db import Base

Model = TypeVar("Model", bound=Base)
Schema = TypeVar("Schema", bound=BaseModel)
CreateSchema = TypeVar("CreateSchema", bound=BaseModel)
UpdateSchema = TypeVar("UpdateSchema", bound=BaseModel)


class CRUD(Generic[Model, Schema, CreateSchema, UpdateSchema]):
    """CRUD.

    Base crud class
    """

    def __init__(self, *, orm_class: Type[Model], schema_class: Type[Schema]):
        self.orm_class = orm_class
        self.schema_class = schema_class

    def create(self, *, session: Session, obj: CreateSchema) -> Schema:
        """create.

        Create a new object

        Args:
            session (Session): database session
            obj (CreateSchema): obj to create

        Returns:
            None:
        """
        orm_model = self.orm_class(**obj.dict())  # type: ignore
        session.add(orm_model)
        session.commit()
        return self.schema_class.from_orm(orm_model)

    def get(self, *, session: Session, identifier: UUID) -> Schema:
        """get.

        Args:
            session (Session): database session
            identifier (UUID): identifier to get by

        Returns:
            Schema: obj in database

        Raises:
            sqlalchemy.orm.exc.NoResultFound: if no results were found
            sqlalchemy.orm.exc.MultipleResultsFound: if multiple results were found
        """
        return self.schema_class.from_orm(session.query(self.orm_class).get(identifier))

    def get_all(self, *, session: Session) -> List[Schema]:
        """get_all.

        Args:
            session (Session): database session

        Returns:
            List[Schema]: objs in database
        """
        return [
            self.schema_class.from_orm(x) for x in session.query(self.orm_class).all()
        ]

    def delete(self, *, session: Session, identifier: UUID) -> Schema:
        """delete.

        Args:
            session (Session): database session
            identifier (UUID): identifier to delete

        Returns:
            OrmSchema: obj in database

        Raises:
            sqlalchemy.orm.exc.NoResultFound: if no results were found
            sqlalchemy.orm.exc.MultipleResultsFound: if multiple results were found
        """
        obj = session.query(self.orm_class).get(identifier)
        session.delete(obj)
        session.commit()
        return self.schema_class.from_orm(obj)

    def update(
        self, *, session: Session, identifier: UUID, update: UpdateSchema
    ) -> Schema:
        """update.
        Update object in db.

        Args:
            session (Session): database session
            identifier (UUID): identifier to update
            update (UpdateSchema): update data

        Returns:
            OrmSchema: obj in database

        Raises:
            sqlalchemy.orm.exc.NoResultFound: if no results were found
            sqlalchemy.orm.exc.MultipleResultsFound: if multiple results were found
        """
        update_dict = update.dict(exclude_unset=True)
        obj = session.query(self.orm_class).get(identifier)

        for key, value in update_dict.items():
            setattr(obj, key, value)

        session.commit()
        return self.schema_class.from_orm(obj)
