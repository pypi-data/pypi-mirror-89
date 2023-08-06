# -*- coding: utf-8 -*-
"""
    fiber.schema.orm.user
    ~~~~~~~~~~

    Schema definitions for user model

    :copyright: (c) 2020 by Robin Raymond.
    :license: MIT, see LICENSE for more details.
"""

# pylint: disable=no-name-in-module
# pylint: disable=no-self-argument
from pydantic import BaseModel

from .base import ORMSchema


class UserBase(BaseModel):
    """UserBase.

    User base schema
    """

    reference: str


class UserCreate(UserBase):
    """UserCreate.

    Create user schema
    """


class UserUpdate(UserBase):
    """UserUpdate.

    Update user schema
    """


class UserDB(ORMSchema, UserBase):
    """User.

    User schema
    """
