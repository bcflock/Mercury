
from mercury.logger.DebugLogger import DebugLogger

_logger = DebugLogger(__file__)

class _URL():
    def __init__(self, Pattern, Value):
        _logger.log(msg="Initalizing", fname="_URL.init()",
                    kwargs={"Pattern":Pattern, "Value": Value})

        self.Pattern = Pattern
        self.Value = Value
        pass
    def __str__(self):
        return 'URL: {self.Pattern}, {self.Value}'
        
    