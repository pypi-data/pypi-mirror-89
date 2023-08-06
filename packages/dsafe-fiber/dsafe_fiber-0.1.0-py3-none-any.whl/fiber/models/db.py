# -*- coding: utf-8 -*-
"""
    fiber.db
    ~~~~~~~~

    Base class for ORM models

    :copyright: (c) 2020 by Robin Raymond.
    :license: MIT, see LICENSE for more details.
"""

import datetime
import re
import uuid

from sqlalchemy import Column, DateTime
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.ext.declarative import declarative_base, declared_attr


def to_snake(string: str) -> str:
    """to_snake.

    Args:
        string (str): input

    Returns:
        str: snake version of input
    """
    return re.sub(r"(?<!^)(?=[A-Z])", "_", string).lower()


class CustomBase:
    """CustomBase.

    Base class for ORM modules.
    """

    __name__: str

    @declared_attr
    def __tablename__(self) -> str:
        return to_snake(self.__name__)

    id = Column(
        UUID(as_uuid=True),
        default=uuid.uuid4,
        primary_key=True,
        unique=True,
        nullable=False,
    )

    created_at = Column(DateTime, default=datetime.datetime.utcnow, nullable=False)
    updated_at = Column(
        DateTime,
        default=datetime.datetime.utcnow,
        onupdate=datetime.datetime.utcnow,
        nullable=False,
    )


Base = declarative_base(cls=CustomBase)
