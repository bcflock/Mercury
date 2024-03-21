

from mercury.config_parser.DataTypes.Types import _Parameter, _Source, _Payload, _URL

from mercury.logger.DebugLogger import DebugLogger

_logger = DebugLogger(__file__)

class ParameterDeclaration:
    def __init__(self, DataRoot, TabLevel=1, TabWidth=4):
        _logger.log(msg="Initalizing", fname="ParameterDeclaration.init()",
                    kwargs={"DataRoot":DataRoot, "TabLevel": TabLevel, "TabWidth": TabWidth})

        self.DataRoot = DataRoot
        self.TabWidth = TabWidth 
        self.TabLevel = TabLevel
    # Parameter Declaration
    def declare(self, Parameter: _Parameter):
        self.Parameter = Parameter
        return f'''{" "*self.TabWidth*self.TabLevel}{Parameter.Key} = {self.SourceToString(Parameter.Source)}'''
    def SourceToString(self, source: _Source):
        if source == None:
            return f'event.{self.DataRoot}.{self.Parameter.Key}'
        if source.type == "URL":
            return self.URLSourceToString(source.source)
        if source.type == "Payload":
            return self.PayloadSourceToString(source.source)

    def PayloadSourceToString(self, Payload: _Payload):
        DataRoot = f'{self.DataRoot}.' if Payload.UseDataRoot else ""
        return f'''event.{DataRoot}{Payload.Path}'''
    
    def URLSourceToString(self, URL:_URL):
        return f'''re.sub('{URL.Pattern}', r'{URL.Value}', payload.path)'''
