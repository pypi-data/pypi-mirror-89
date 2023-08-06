# -*- coding: utf-8 -*-
"""
    fiber.config
    ~~~~~~~~~~~~

    Configuration modul to load settings

    :copyright: (c) 2020 by Robin Raymond.
    :license: MIT, see LICENSE for more details.
"""

# pylint: disable=no-name-in-module
# pylint: disable=no-self-argument
from pydantic import AnyHttpUrl, BaseModel, PostgresDsn


class Config(BaseModel):
    """Config.
    General configuration
    """

    HTTP_ENDPOINT: AnyHttpUrl
    POSTGRESQL_ENDPOINT: PostgresDsn
