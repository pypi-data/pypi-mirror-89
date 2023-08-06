# -*- coding: utf-8 -*-
"""
    fiber.crud.contract
    ~~~~~~~~~~

    Contract CRUD.

    :copyright: (c) 2020 by Robin Raymond.
    :license: MIT, see LICENSE for more details.
"""
from fiber.models.contract import Contract
from fiber.schemas.orm.contract import ContractBase, ContractDB

from .base import CRUD


class CRUDContract(CRUD[Contract, ContractDB, ContractBase, ContractBase]):
    """CRUDContract.

    Contract crud class
    """


crud_contract = CRUDContract(orm_class=Contract, schema_class=ContractDB)
