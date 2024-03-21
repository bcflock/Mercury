

from mercury.config_parser.DataTypes.Mercury.Function import _Function

class Model:
    def __init__(self, ** kwargs):
        print("mercury.config_parser - Model.init() with: ", "\n  **kwargs: ", kwargs)
        self.Functions = [_Function(k, v) for k, v in kwargs['Functions'].items()]
    def __str__(self):
        return '\n'.join([str(f) for f in self.Functions])
