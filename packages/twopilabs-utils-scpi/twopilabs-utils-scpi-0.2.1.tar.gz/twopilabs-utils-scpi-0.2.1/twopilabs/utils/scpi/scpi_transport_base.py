import abc
from typing import *

class ScpiTransportBase(object):
    __metaclass__ = abc.ABCMeta

    @abc.abstractmethod
    def reset(self) -> None:
        raise NotImplementedError("Please Implement this method")

    @abc.abstractmethod
    def readline(self, size: int = -1) -> str:
        raise NotImplementedError("Please Implement this method")

    @abc.abstractmethod
    def writeline(self, line: str) -> Optional[int]:
        raise NotImplementedError("Please Implement this method")