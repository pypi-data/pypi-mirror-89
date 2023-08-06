from .scpi_types import ScpiEvent

class ScpiException(Exception):
    def __init__(self, *args, **kwargs):
        super().__init__(self, *args, **kwargs)

class ScpiErrorException(ScpiException):
    def __init__(self, scpi_error: ScpiEvent = None):
        self.scpi_error = scpi_error
        super().__init__(self, str(self))

    def __str__(self):
        return f'SCPI Error {self.scpi_error.code}: {self.scpi_error.description}' \
               + f' ({self.scpi_error.info})' if self.scpi_error.info is not None else ''