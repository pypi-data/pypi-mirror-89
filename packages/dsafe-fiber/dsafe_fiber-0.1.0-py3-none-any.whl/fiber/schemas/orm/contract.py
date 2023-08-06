# -*- coding: utf-8 -*-
"""
    fiber.schema.orm.contract
    ~~~~~~~~~~

    Schema definitions for contract model

    :copyright: (c) 2020 by Robin Raymond.
    :license: MIT, see LICENSE for more details.
"""

# pylint: disable=no-name-in-module
# pylint: disable=no-self-argument
from uuid import UUID

from pydantic import BaseModel

from .base import ORMSchema


class ContractBase(BaseModel):
    """ContractBase.

    Contract base schema
    """

    address: str
    user_id: UUID


class ContractDB(ORMSchema, ContractBase):
    """Contract.

    Contract db schema
    """
