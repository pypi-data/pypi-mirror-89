# -*- coding: utf-8 -*-
"""
    fiber.user
    ~~~~~~~~~~

    User ORM models

    :copyright: (c) 2020 by Robin Raymond.
    :license: MIT, see LICENSE for more details.
"""

from typing import TYPE_CHECKING

from sqlalchemy import Column, String
from sqlalchemy.orm import relationship

from .db import Base

if TYPE_CHECKING:
    from .project import Project  # noqa: F401 # pragma: nocover
    from .tag import Tag  # noqa: F401 # pragma: nocover


class User(Base):
    """User.

    User orm class. A user is a way to manage access rights. Also provides
    automatic filters.
    """

    reference = Column(String, nullable=False, index=True, unique=True)

    projects = relationship(
        "Project",
        back_populates="user",
        cascade="all, delete",
        passive_deletes=True,
    )
    tags = relationship(
        "Tag",
        back_populates="user",
        cascade="all, delete",
        passive_deletes=True,
    )
