


from mercury.config_parser.DataTypes.Mercury.Source import _Source
from mercury.config_parser.DataTypes.Type import _Type


from mercury.logger.DebugLogger import DebugLogger

_logger = DebugLogger(__file__)



class _Parameter():
    def __init__(self, 
                 Key, 
                 Type, 
                 Identifier = False,
                 Source = None, 
                 Column = None,
                 **kwargs):  
                
                _logger.log(msg="Initalizing", fname="_Parameter.init()",
                            kwargs=({
                                   "Key": Key,
                                   "Type":Type, 
                                   "Identifier": Identifier,
                                   "Source": Source,
                                   "Column": Column
                            } | kwargs)) # | operator adds two dicts s.t. {a: 1} | {b: 2} = {a:1, b: 2}

                self.Key = Key
                self.Type = _Type(Type)
                self.Identifier = Identifier
                self.Source = _Source(Source) if Source else None
                self.Column = Column if Column else Key
    def __str__(self):
        return f'''Parameter {self.Key}: {self.Type}, {self.Identifier}, {self.Source}, {self.Column}'''
