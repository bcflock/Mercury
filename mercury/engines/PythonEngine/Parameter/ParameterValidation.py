


from mercury.config_parser.DataTypes.Types import _Parameter, _Integer, _String, _Type

from mercury.config_parser.Handlers.Handlers import _OnFail

from mercury.logger.DebugLogger import DebugLogger

_logger = DebugLogger(__file__)


class ParameterValidation:
    def __init__(self, TabLevel=1, TabWidth=4):
        _logger.log(msg="Initalizing", fname="ParameterValidation.init()",
                    kwargs={"TabLevel": TabLevel, "TabWidth": TabWidth})

        self.content = ""
        self.TabLevel = TabLevel
        self.TabWidth = TabWidth

    def validate(self, Parameter: _Parameter):
        self.Parameter = Parameter 
        self.Name : str = self.Parameter.Key
        self.Type : _Type= self.Parameter.Type
        return self.validateType()
    
    def validateType(self):
        _logger.log(msg="Validating Type", fname="ParameterValidation.validateType()")
        if isinstance(self.Type.Type, _Integer):
            return self.validateInt()
        elif isinstance(self.Type.Type, _String):
            return self.validateString()
        else: return ""

    def fail(self, failure: _OnFail):
        return f'{" "*self.TabLevel*self.TabWidth}'\
            +'return {"statusCode": '\
            + str(failure.Code) \
            + ', "body": {"message": ' \
            + f'"{failure.Message}"' \
            + '}}'
    
    
    def validateInt(self):
        _logger.log(msg="Validating Integer", fname="ParameterValidation.validateInt()")

        return f'\n{" "*self.TabWidth*self.TabLevel}' + f'\n{" "*self.TabWidth*self.TabLevel}'.join([
            f'try:',
            f'{" "*self.TabWidth*self.TabLevel}{self.Name} = int({self.Name})',
            f'except TypeError:',
            self.fail(self.Type.castFail),
            f'if not {self.Type.Type.Lower} < {self.Name} < {self.Type.Type.Upper}:',
            self.fail(self.Type.Type.ValidationFail),
        ])
    

    def validateString(self):
        _logger.log(msg="Validating String", fname="ParameterValidation.validateString()")

        return f'\n{" "*self.TabWidth*self.TabLevel}' + \
            f'\n{" "*self.TabWidth*self.TabLevel}'.join([
                f'if not {self.Type.Type.Lower} < len({self.Name}) < {self.Type.Type.Upper}:',
                self.fail(self.Type.Type.LengthFail),
                f'if not re.fullmatch(r"{self.Type.Type.Pattern}",{self.Name}):',
                self.fail(self.Type.Type.PatternFail)
            ])
