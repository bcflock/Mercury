

from mercury.config_parser.DataTypes.Mercury.Table import _Table
from mercury.config_parser.DataTypes.Mercury.Query import _Query
from mercury.config_parser.DataTypes.Mercury.Parameter import _Parameter



from mercury.logger.DebugLogger import DebugLogger

_logger = DebugLogger(__file__)


class _Function:
    def __init__(self, name, config):
        _logger.log(msg="Initalizing", fname="_Function.init()",kwargs={"name":name, "config": config})
        self.Name = name
        self.Methods = config['Method'] #method is required
        self.DataRoot = config.get('DataRoot')
        #TODO: Either rename or make this support multiple tables
        self.Tables = [_Table(k, **v) for k, v in config.get('Tables', {}).items()][0]
        self.Parameters = {_Parameter(k, **v) for k, v in config.get('Parameters', {}).items()}
        self.Query = _Query(**config.get('Query', {'Override': ''}))
    def __str__(self) -> str:
        return ('Function ' + str(self.Name) + '\n' + 
            f'''Supported Methods: {self.Methods}''' + '\n' + 
            f'''Dataroot: {self.DataRoot}''' + '\n' + 
            f'Tables: ' + '\n\t\t' + '\n\t\t'.join([str(s) for s in [self.Tables]])  + '\n' + 
            f'Parameters:' + '\n\t\t' + '\n\t\t'.join([str(v) for v in self.Parameters]))

