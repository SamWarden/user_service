from abc import ABC
from typing import Generic, TypeVar

import didiator

CRes = TypeVar("CRes")


class Command(didiator.Command[CRes], ABC, Generic[CRes]):
    pass


C = TypeVar("C", bound=Command)


class CommandHandler(didiator.CommandHandler[C, CRes], ABC, Generic[C, CRes]):
    pass
