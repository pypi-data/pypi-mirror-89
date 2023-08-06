# -*- coding: utf-8 -*-
"""
    fiber.crud.tag
    ~~~~~~~~~~

    Tag CRUD.

    :copyright: (c) 2020 by Robin Raymond.
    :license: MIT, see LICENSE for more details.
"""
from typing import List
from uuid import UUID

from sqlalchemy.orm import Session

from fiber.models.tag import Tag
from fiber.schemas.orm.tag import TagBase, TagDB

from .base import CRUD


class CRUDTag(CRUD[Tag, TagDB, TagBase, TagBase]):
    """CRUDTag.

    Tag crud class
    """

    def get_by_name(self, *, session: Session, name: str, user_id: UUID) -> TagDB:
        """get_by_name.

        Args:
            session (Session): database session
            name (str): name of tag
            user_id (UUID): user id

        Returns:
            TagDB: tag in db

        Raises:
            sqlalchemy.orm.exc.NoResultFound: if no results were found
            sqlalchemy.orm.exc.MultipleResultsFound: if multiple results were found
        """
        return TagDB.from_orm(
            session.query(self.orm_class)
            .filter(self.orm_class.user_id == user_id)
            .filter(self.orm_class.name == name)
            .one()
        )

    def get_all_of_user(self, *, session: Session, user_id: UUID) -> List[TagDB]:
        """get_all_of_user.

        Args:
            session (Session): database session session
            user_id (UUID): user_id of user

        Returns:
            List[TagDB]:
        """
        return [
            TagDB.from_orm(x)
            for x in session.query(self.orm_class)
            .filter(self.orm_class.user_id == user_id)
            .all()
        ]


crud_tag = CRUDTag(orm_class=Tag, schema_class=TagDB)
