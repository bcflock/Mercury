


from mercury.config_parser.DataTypes.Mercury.Source import _Source
from mercury.config_parser.DataTypes.Type import _Type




class _Parameter():
    def __init__(self, 
                 Key, 
                 Type, 
                 Identifier = False,
                 Source = None, 
                 Column = None,
                 **kwargs):  
                
                print("mercury.config_parser - _Parameter.init() with: ", "\n  Key: ", Key, "\n  Type: ", Type, "\n  Identifier: ", Identifier, "\n  Source: ", Source, "\n  Column: ", Column, "\n **kwargs: ", kwargs)
                self.Key = Key
                self.Type = _Type(Type)
                self.Identifier = Identifier
                self.Source = _Source(Source) if Source else None
                self.Column = Column if Column else Key
    def __str__(self):
        return f'''Parameter {self.Key}: {self.Type}, {self.Identifier}, {self.Source}, {self.Column}'''
