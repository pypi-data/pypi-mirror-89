# -*- coding: utf-8 -*-
"""
    fiber.schemas.orm.base
    ~~~~~~~~~~

    Base utiltites for schemas

    :copyright: (c) 2020 by Robin Raymond.
    :license: MIT, see LICENSE for more details.
"""
# pylint: disable=no-name-in-module
# pylint: disable=no-self-argument
from datetime import datetime
from uuid import UUID

from pydantic import BaseModel


class ORMSchema(BaseModel):
    """ORMSchema.

    Bas ORM schema
    """

    id: UUID
    created_at: datetime
    updated_at: datetime

    class Config:
        """Config."""

        orm_mode = True
