# -*- coding: utf-8 -*-
"""
    fiber.crud.user
    ~~~~~~~~~~

    User CRUD.

    :copyright: (c) 2020 by Robin Raymond.
    :license: MIT, see LICENSE for more details.
"""
from sqlalchemy.orm import Session

from fiber.models.user import User
from fiber.schemas.orm.user import UserCreate, UserDB, UserUpdate

from .base import CRUD


class CRUDUser(CRUD[User, UserDB, UserCreate, UserUpdate]):
    """CRUDUser.

    User crud class
    """

    def get_by_reference(self, *, session: Session, reference: str) -> UserDB:
        """get_by_reference.

        Args:
            session (Session): database session
            reference (str): unique reference

        Returns:
            UserDB: user in db

        Raises:
            sqlalchemy.orm.exc.NoResultFound: if no results were found
            sqlalchemy.orm.exc.MultipleResultsFound: if multiple results were found
        """
        obj = (
            session.query(self.orm_class)
            .filter(self.orm_class.reference == reference)
            .one()
        )

        return UserDB.from_orm(obj)


crud_user = CRUDUser(orm_class=User, schema_class=UserDB)
