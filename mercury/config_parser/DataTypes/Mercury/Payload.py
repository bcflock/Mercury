

from mercury.logger.DebugLogger import DebugLogger

_logger = DebugLogger(__file__)


class _Payload():
    def __init__(self, Path, DataRoot=True):
        _logger.log(msg="Initalizing", fname="_Payload.init()",kwargs={"Path":Path, "DataRoot": DataRoot})

        self.Path = Path
        self.UseDataRoot = DataRoot
        pass
    def __str__(self):
        return f'Payload: {self.Path}, {self.UseDataRoot}'

