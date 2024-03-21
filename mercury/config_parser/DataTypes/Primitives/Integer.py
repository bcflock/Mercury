

from mercury.config_parser.Handlers.OnFail import _OnFail

class _Integer:
    def __init__(self, Bounds={}, **kwargs):
        self.Lower = Bounds.get('Lower', "float('-inf')")
        self.Upper = Bounds.get('Upper', "float('inf')")
        self.ValidationFail = _OnFail(**Bounds.get('OnFail', {"Code":400}))
    def __str__(self):
        return f'({type(self).__name__}: Bounds [{self.Lower}, {self.Upper}] Failure:{bool(_OnFail)})'

        