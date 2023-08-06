# -*- coding: utf-8 -*-
"""
    fiber.client.user
    ~~~~~~~~~~

    User client definition

    :copyright: (c) 2020 by Robin Raymond.
    :license: MIT, see LICENSE for more details.
"""

from typing import List

from sqlalchemy.orm import Session
from sqlalchemy.orm.exc import NoResultFound

from fiber import crud
from fiber.schemas.orm.user import UserCreate, UserDB, UserUpdate


class UserClient:
    """UserClient.

    Client class to manipulate users
    """

    def __init__(self, session: Session) -> None:
        self._session = session

    def get_or_create_user(self, name: str) -> UserDB:
        """get_or_create_user.

        Args:
            name (str): Outside reference of the user

        Returns:
            UserDB: user in database
        """

        try:
            return crud.crud_user.get_by_reference(
                session=self._session, reference=name
            )
        except NoResultFound:
            return crud.crud_user.create(
                session=self._session, obj=UserCreate(reference=name)
            )

    def remove_user(self, name: str) -> UserDB:
        """remove_user.

        Args:
            name (str): Outside reference of the user

        Returns:
            UserDB: user in database
        """

        user = crud.crud_user.get_by_reference(session=self._session, reference=name)
        return crud.crud_user.delete(session=self._session, identifier=user.id)

    def rename_user(self, old_name: str, new_name: str) -> UserDB:
        """rename_user.
        Rename a user

        Args:
            old_name (str): old name of user
            new_name (str): new name of user

        Returns:
            UserDB: user in database
        """
        user = crud.crud_user.get_by_reference(
            session=self._session, reference=old_name
        )

        return crud.crud_user.update(
            session=self._session,
            identifier=user.id,
            update=UserUpdate(reference=new_name),
        )

    def get_all_users(self) -> List[UserDB]:
        """get_all_users.

        Returns:
            List[UserDB]:
        """
        return crud.crud_user.get_all(session=self._session)
