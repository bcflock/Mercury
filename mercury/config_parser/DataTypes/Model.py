

from mercury.config_parser.DataTypes.Mercury.Function import _Function

from mercury.logger.DebugLogger import DebugLogger

_logger = DebugLogger(__file__)

class Model:
    def __init__(self, ** kwargs):
        _logger.log(msg="Initalizing", fname="Model.init()",kwargs=kwargs)

        self.Functions = [_Function(k, v) for k, v in kwargs['Functions'].items()]
    def __str__(self):
        return '\n'.join([str(f) for f in self.Functions])
