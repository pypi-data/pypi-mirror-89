# -*- coding: utf-8 -*-
"""
    fiber.models.tag
    ~~~~~~~~~~~~~~

    Tag ORM models

    :copyright: (c) 2020 by ROBIN RAYMOND.
    :license: MIT, see LICENSE for more details.
"""

from typing import TYPE_CHECKING

from sqlalchemy import Column, ForeignKey, String, Table
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from .db import Base

if TYPE_CHECKING:
    from .contract import Contract  # noqa: F401 # pragma: nocover
    from .user import User  # noqa: F401 # pragma: nocover


contract_tag_association = Table(
    "contract_tag_association",
    Base.metadata,
    Column("tag_id", UUID(as_uuid=True), ForeignKey("tag.id"), nullable=False),
    Column(
        "contract_id", UUID(as_uuid=True), ForeignKey("contract.id"), nullable=False
    ),
)


class Tag(Base):
    """Tag.

    A tag to group smart contracts in the database
    """

    name = Column(String, nullable=False)

    user_id = Column(UUID(as_uuid=True), ForeignKey("user.id", ondelete="CASCADE"))
    user = relationship("User", back_populates="tags")

    contracts = relationship(
        "Contract", secondary=contract_tag_association, back_populates="tags"
    )
