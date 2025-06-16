"""This is the module that defines the types.
"""

import enum
from typing import Any

from pydantic import BaseModel, Field


class ParamKey(enum.StrEnum):
    """Defines the dictionary key for the main parameters.
    """
    HANDLER = enum.auto()
    LEVEL = enum.auto()
    PARAM = enum.auto()
    RESULT = enum.auto()
    MODE = enum.auto()
    THEME = enum.auto()


class SessionType(enum.StrEnum):
    """Defines the session types.
    """
    WAIT = enum.auto()
    WORK = enum.auto()
    BREAK = enum.auto()
    PAUSE = enum.auto()
