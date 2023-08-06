import logging
from typing import *
from .scpi_transport_serial import ScpiSerialTransport
from .scpi_type_base import ScpiTypeBase

logger = logging.getLogger(__name__)


class ScpiDevice(object):
    def __init__(self, resource: str) -> None:
        self.resource = resource
        self.transport = ScpiSerialTransport(resource)
        logger.info(f'open (resource): {resource}')

    def is_open(self):
        return self.transport.is_open

    def close(self) -> None:
        self.transport.close()

    def reset(self) -> None:
        self.transport.reset()

    def execute(self, header: str, param = None, result = type(None)) -> Type[ScpiTypeBase]:
        command = header
        resp = None
        response = None

        if param is not None:
            command = ' '.join([header, param.compose()])

        self.transport.writeline(command)

        if result is not type(None):
            response = result.parse(self.transport)
            resp = str(response)

        logger.info(f'exec [{type(param).__name__}] -> [{result.__name__ }]: <{command}> -> ({resp})')
        return response

