# -*- coding: utf-8 -*-
"""
    fiber.models.contract
    ~~~~~~~~~~~~~~

    Project ORM models

    :copyright: (c) 2020 by ROBIN RAYMOND.
    :license: MIT, see LICENSE for more details.
"""

from typing import TYPE_CHECKING

from sqlalchemy import Column, ForeignKey, String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from .db import Base

if TYPE_CHECKING:
    from .contract import Contract  # noqa: F401 # pragma: nocover
    from .user import User  # noqa: F401 # pragma: nocover


class Project(Base):
    """Project.

    A project in the database
    """

    name = Column(String, nullable=False)

    user_id = Column(UUID(as_uuid=True), ForeignKey("user.id", ondelete="CASCADE"))
    user = relationship("User", back_populates="projects")

    contracts = relationship("Contract", back_populates="project")
