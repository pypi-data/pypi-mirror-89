# -*- coding: utf-8 -*-
"""
    fiber.client.tag
    ~~~~~~~~~~

    Tag client definition

    :copyright: (c) 2020 by Robin Raymond.
    :license: MIT, see LICENSE for more details.
"""

from typing import List
from uuid import UUID

from sqlalchemy.orm import Session
from sqlalchemy.orm.exc import NoResultFound

from fiber import crud
from fiber.schemas.orm.tag import TagCreate, TagDB, TagUpdate


class TagClient:
    """TagClient.

    Client class to manipulate users
    """

    def __init__(self, session: Session, user_id: UUID) -> None:
        self._session = session
        self._user_id = user_id

    def get_or_create_tag(self, name: str) -> TagDB:
        """get_or_create_tag.

        Args:
            name (str): name of tag

        Returns:
            TagDB: tag in database
        """

        try:
            return crud.crud_tag.get_by_name(
                session=self._session, name=name, user_id=self._user_id
            )
        except NoResultFound:
            return crud.crud_tag.create(
                session=self._session, obj=TagCreate(name=name, user_id=self._user_id)
            )

    def remove_tag(self, name: str) -> TagDB:
        """remove_tag.

        Args:
            name (str): tag name

        Returns:
            TagDB: tag in database
        """

        tag = crud.crud_tag.get_by_name(
            session=self._session, name=name, user_id=self._user_id
        )
        return crud.crud_tag.delete(session=self._session, identifier=tag.id)

    def rename_tag(self, old_name: str, new_name: str) -> TagDB:
        """rename_tag.
        Rename a tag

        Args:
            old_name (str): old name of tag
            new_name (str): new name of tag

        Returns:
            UserDB: user in database
        """
        tag = crud.crud_tag.get_by_name(
            session=self._session, name=old_name, user_id=self._user_id
        )

        return crud.crud_tag.update(
            session=self._session,
            identifier=tag.id,
            update=TagUpdate(name=new_name),
        )

    def get_all_tags(self) -> List[TagDB]:
        """get_all_tags.
        Get all tags of user

        Returns:
            List[TagDB]:
        """
        return crud.crud_tag.get_all_of_user(
            session=self._session, user_id=self._user_id
        )
