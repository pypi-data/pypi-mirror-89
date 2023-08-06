# -*- coding: utf-8 -*-
"""
    fiber.tag
    ~~~~~~~~~

    Tag ORM Schemas

    :copyright: (c) 2020 by Robin Raymond.
    :license: MIT, see LICENSE for more details.
"""

from typing import Optional
# pylint: disable=no-name-in-module
# pylint: disable=no-self-argument
from uuid import UUID

from pydantic import BaseModel

from .base import ORMSchema


class TagBase(BaseModel):
    """TagBase.

    Tag base schema
    """

    name: str
    user_id: Optional[UUID]


class TagCreate(TagBase):
    """TagCreate.

    Tag create schema
    """

    user_id: UUID


class TagUpdate(TagBase):
    """TagUpdate.

    Tag update schema
    """


class TagDB(ORMSchema, TagBase):
    """TagDB.

    Tagdb schema
    """

    user_id: UUID
