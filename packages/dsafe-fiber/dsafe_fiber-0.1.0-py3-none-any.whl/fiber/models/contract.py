# -*- coding: utf-8 -*-
"""
    fiber.models.contract
    ~~~~~~~~~~~~~~

    Contract ORM models

    :copyright: (c) 2020 by ROBIN RAYMOND.
    :license: MIT, see LICENSE for more details.
"""

from typing import TYPE_CHECKING

from sqlalchemy import Column, ForeignKey, String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from .db import Base
from .tag import contract_tag_association

if TYPE_CHECKING:
    from .project import Project  # noqa: F401 # pragma: nocover
    from .tag import Tag  # noqa: F401 # pragma: nocover


class Contract(Base):
    """Contract.

    A smart contract in the database
    """

    address = Column(String, nullable=False, index=True)

    project_id = Column(
        UUID(as_uuid=True), ForeignKey("project.id", ondelete="CASCADE")
    )
    project = relationship("Project", back_populates="contracts")

    tags = relationship(
        "Tag", secondary=contract_tag_association, back_populates="contracts"
    )
