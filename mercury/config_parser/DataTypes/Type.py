

from mercury.config_parser.Handlers.OnFail import _OnFail
from mercury.config_parser.DataTypes.Primitives.Integer import _Integer
from mercury.config_parser.DataTypes.Primitives.String import _String


class _Type():
    def __init__(self, Type : dict):
        keys = list(Type.keys())
        if len(keys) < 1:
            raise TypeError
        if 'String' in keys:
            self.Type = _String(**Type['String'] or {})
        elif 'Integer' in keys:
            self.Type = _Integer(**Type['Integer'] or {})
        else:
            raise ValueError
        self.castFail = _OnFail(**Type.get('OnFail', {"Code":400}))
    def __str__(self):
        return f'Type: {str(self.Type)}'
