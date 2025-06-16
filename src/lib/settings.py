"""This is the module that defines the configuration.
"""

import zoneinfo
from logging import CRITICAL, DEBUG, ERROR, INFO, WARNING
from typing import ClassVar

from pydantic import BaseModel, Field

#: ZoneInfo class.
ZoneInfo = zoneinfo.ZoneInfo(key='Asia/Tokyo')


class ParamLog(BaseModel):
    """Defines the parameters used in the logging configuration.
    """
    SH: str = Field(default='sh', frozen=True)
    FH: str = Field(default='fh', frozen=True)
    #: str: The name to pass to ``logging.getLogger``.
    NAME: str = 'main'
    HANDLER: ClassVar[dict[str, bool]] = {
        SH: True,
        FH: True,
    }
    #: ClassVar[dict[str, int]]: Log level.
    #:
    #: *    key=sh: stream handler.
    #: *    key=fh: file handler.
    LEVEL: ClassVar[dict[str, int]] = {
        SH: DEBUG,
        FH: DEBUG,
    }
    #: str: File path.
    FPATH: str = 'log/log.txt'
    #: int: Max file size.
    SIZE: int = Field(default=int(1e+6), gt=0)
    #: int: Number of files.
    NUM: int = Field(default=10, gt=0)

    class Config:
        validate_assignment = True
        extra = 'forbid'
