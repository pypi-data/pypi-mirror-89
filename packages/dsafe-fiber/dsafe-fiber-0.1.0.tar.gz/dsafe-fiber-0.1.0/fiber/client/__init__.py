# -*- coding: utf-8 -*-
"""
    fiber.client.__init__
    ~~~~~~~~~~~~~~

    Fiber client definition

    :copyright: (c) 2020 by Robin Raymond.
    :license: MIT, see LICENSE for more details.
"""

from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker

from fiber.config import Config
from fiber.schemas.orm.user import UserDB

from .tag import TagClient
from .user import UserClient


class Client:
    """Client.

    Main class to use fiber
    """

    def __init__(self, config: Config) -> None:
        self._config = config
        engine = create_engine(config.POSTGRESQL_ENDPOINT)
        session = sessionmaker(bind=engine)
        self._session = session()

    def get_session(self) -> Session:
        """get_session.
        Get db session

        Args:

        Returns:
            Session:
        """
        return self._session

    def get_user_client(self) -> UserClient:
        """get_user_client.
        Get a user client

        Args:

        Returns:
            UserClient: user client
        """
        return UserClient(self._session)

    def get_tag_client(self, user: UserDB) -> TagClient:
        """get_tag_client.
        Get a tag client

        Args:
            user (UserDB): user to initialize the tag client for

        Returns:
            TagClient: tag client
        """
        return TagClient(session=self._session, user_id=user.id)
