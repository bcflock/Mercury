import yaml
import json
from types import SimpleNamespace
from collections import defaultdict

#TODO: There should be a refactor that takes advantage of yaml tags for directly creating the objects

VERSION = "0.0.2"
Patterns = {
    'URL': r'^(?:(http|https):\/\/)([\w.-]+)(\.[\w.-]+)+([\/\w\.-]*)*\/?$',
    'Email': r'^[a-zA-Z0-9]+(?:\.[a-zA-Z0-9]+)*@[a-zA-Z0-9]+(?:\.[a-zA-Z0-9]+)*$'
}

class ConfigParser:
    def parse(config):
        with open(config, 'r') as f:
            inputstring = f.read()
            model = Model(**yaml.safe_load( inputstring )) 
        return model

class Model:
    def __init__(self, ** kwargs):
        self.Functions = [_Function(k, v) for k, v in kwargs['Functions'].items()]
    def __str__(self):
        return f'''Model:
        {'\n'.join([str(f) for f in self.Functions])}
    '''
class _Function:
    def __init__(self, name, config):
        self
        self.Name = name
        self.Methods = config['Method'] #method is required
        self.DataRoot = config.get('DataRoot')
        #TODO: Either rename or make this support multiple tables
        self.Tables = [_Table(k, **v) for k, v in config.get('Tables', {}).items()][0]
        self.Parameters = {_Parameter(k, **v) for k, v in config.get('Parameters', {}).items()}
        self.Query = _Query(**config.get('Query', {'Override': ''}))
    def __str__(self):
        return f'''Function {self.Name}: 
        Supported Methods: {self.Methods}
        Dataroot: {self.DataRoot}
        Tables: \n\t\t{'\n\t\t'.join([str(s) for s in self.Tables])}
        Parameters: \n\t\t{'\n\t\t'.join([f'{str(v)}' for _, v in self.Parameters])}'''

class _Table:
    def __init__(self, Key, Name, Alias, Default = False):
        self.Key = Key
        self.Name = Name
        self.Alias = Alias
        self.Default = Default
    def __str__(self):
        return f"Table {self.Key}: {self.Name}, {self.Alias}, {self.Default}"

class _Query:
    def __init__(self, Type="", Override=""):
        print("Type:",Type)
        print("Override:",Override)
        if not Type and not Override:
           raise ValueError 
        Type = Type.upper()
        if Type:
            print(Type)
            if Type == "SELECT":
                self.query = '''
                    SELECT 
                        {mercury::query::select::parameters}
                    FROM 
                        {mercury::query::tables}
                    WHERE 
                        {mercury::query::identifier}
                    '''
            elif Type == "UPDATE":
                self.query = '''UPDATE 
                        {mercury::query::tables}
                    SET 
                        {mercury::query::update::parameters}
                    WHERE 
                        {mercury::query::identifier}
'''
            elif Type == "INSERT":
                self.query = '''
                    INSERT INTO 
                        {mercury::query::insert::columns}
                    VALUES 
                        {mercury::query::insert::values}
'''
            else:
                raise ValueError("Missing Query Type and no Override provided")
        if Override:
            self.query = Override     
        if not self.query:
            raise ValueError("Missing Query Type and no Override provided")

        
    def __str__(self):
        return f'Query: {self.query}'
class _Parameter():
    def __init__(self, 
                 Key, 
                 Type, 
                 Identifier = False,
                 Source = None, 
                 Column = None,
                 **kwargs):                 
                self.Key = Key
                self.Type = _Type(Type)
                self.Identifier = Identifier
                self.Source = _Source(Source) if Source else None
                self.Column = Column if Column else Key
    def __str__(self):
        return f'''Parameter {self.Key}: {self.Type}, {self.Identifier}, {self.Source}, {self.Column}'''
        
class _Source():
    def __init__(self, source, source_defaults = ""): 
        if 'URL' in source:
            self.type = "URL"
            self.source = _URL(**source['URL'])
        elif 'Payload' in source:
            self.type = "Payload"
            self.source = _Payload(**source['Payload'])

    def __str__(self):
        return f"Source: {self.type}, {str(self.source)} "


class _URL():
    def __init__(self, QueryStringParam=None, PathParam=None):
        assert not (QueryStringParam and PathParam)
        self.PathParam = PathParam
        self.QueryStringParam = QueryStringParam
        pass
    def __str__(self):
        return 'URL: {self.Pattern}, {self.Value}'
        
    
class _Payload():
    def __init__(self, Path, DataRoot=True):
        self.Path = Path
        self.UseDataRoot = DataRoot
        pass
    def __str__(self):
        return f'Payload: {self.Path}, {self.UseDataRoot}'

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
class _OnFail:
    def __init__(self, Code, Message = "", **kwargs):
        self.Code = Code or 400
        self.Message = Message or ""
    def __str__(self):
        return f'OnFail: {self.Code}, {self.Message}'
class _Integer:
    def __init__(self, Bounds={}, **kwargs):
        self.Lower = Bounds.get('Lower', "float('-inf')")
        self.Upper = Bounds.get('Upper', "float('inf')")
        self.ValidationFail = _OnFail(**Bounds.get('OnFail', {"Code":400}))
    def __str__(self):
        return f'({type(self).__name__}: Bounds [{self.Lower}, {self.Upper}] Failure:{bool(_OnFail)})'

        

class _String:
    def __init__(self, Pattern=None, Length={}, **kwargs):
        self.Lower = Length.get('Lower', 0)
        self.Upper = Length.get('Upper', "float('inf')")
        self.LengthFail = _OnFail(**Length.get('OnFail', {"Code": 400}))
        if Pattern:
            if isinstance(Pattern, str):
                if Pattern in Patterns.keys():
                    self.Pattern = Patterns.get(Pattern)
                else:
                    raise ValueError("Arbitrary Regular Expressions must be in an Expression tag")
                self.PatternFail = _OnFail(Code=400)
            else:
                self.Pattern = Pattern.get("Expression", r"/.*/") or r"/.*/"
                if self.Pattern.startswith('/') and self.Pattern.endswith('/'):
                    self.Pattern = self.Pattern[1:-1]
                else:
                    raise ValueError('Expressions should be formatted using this notation: //')
                self.PatternFail = _OnFail(**Pattern.get("OnFail", {'Code': 400}))
        else: 
            self.Pattern = r'.*'
            self.PatternFail = _OnFail(400)

    def __str__(self):
        return f'({type(self).__name__}: Pattern: /{self.Pattern}/, Length:[{self.Lower}, {self.Upper}])'

class _Float(_Type):
    def __init__(self, Bounds=None):
        raise NotImplementedError()