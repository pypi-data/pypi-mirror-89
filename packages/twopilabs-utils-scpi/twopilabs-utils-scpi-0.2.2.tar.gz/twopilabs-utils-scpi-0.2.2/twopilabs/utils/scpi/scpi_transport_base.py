import abc
from typing import *

class ScpiTransportBase(object):
    __metaclass__ = abc.ABCMeta

    @classmethod
    @abc.abstractmethod
    def find_devices(cls, **kwargs):
        raise NotImplementedError("Please Implement this method")

    @abc.abstractmethod
    def __init__(self, resource, *args, **kwargs):
        super().__init__(resource, *args, **kwargs)

    @abc.abstractmethod
    def is_open(self) -> bool:
        raise NotImplementedError("Please Implement this method")

    def close(self) -> None:
        raise NotImplementedError("Please Implement this method")

    @abc.abstractmethod
    def reset(self) -> None:
        raise NotImplementedError("Please Implement this method")

    @abc.abstractmethod
    def readline(self, size: int = -1) -> str:
        raise NotImplementedError("Please Implement this method")

    @abc.abstractmethod
    def writeline(self, line: str) -> Optional[int]:
        raise NotImplementedError("Please Implement this method")


# TypeVar for type hinting subclasses of ScpiTransportBase
ScpiTransports = TypeVar('ScpiTransports', bound=ScpiTransportBase)