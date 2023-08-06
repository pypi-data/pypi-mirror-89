import serial
import logging
from typing import *
from .scpi_transport_base import ScpiTransportBase

logger = logging.getLogger(__name__)

class ScpiSerialTransport(serial.Serial, ScpiTransportBase):
    def __init__(self, port, timeout = 5):
        super().__init__(port = port, timeout = timeout, exclusive=True)
        self.reset()

    def reset(self) -> None:
        self.reset_input_buffer()
        self.reset_output_buffer()
        self.timeout = 0
        while(self.read() != b''):
            pass
        self.timeout = 5

    def readline(self, size: int = -1) -> str:
        size = None if size == -1 else size
        data = super().read_until(b'\r\n', size=size)
        line = data.decode('ascii').strip('\r\n')
        logger.debug(f'read: {line}<CRLF>')
        return line

    def writeline(self, line: str) -> Optional[int]:
        logger.debug(f'write: {line}<CRLF>')
        data = (line + '\r\n').encode('ascii')
        return super().write(data)