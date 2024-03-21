import mercury.config_parser as config_parser
import re
expr = {
        'parameters': {
            'declare'  : re.compile(r"([\t\s]*){mercury::parameters::declare}"),
            'validate' : re.compile(r"([\t\s]*){mercury::parameters::validate}")
        },
        'query': {
            'declare': re.compile(r"([\t\s]*){mercury::query::declare}"),
            'select': {
                'parameters': re.compile(r"{mercury::query::select::parameters}")
            },
            'update': {
                'parameters': re.compile(r"{mercury::query::update::parameters}")
            },
            'insert': {
                'values': re.compile(r"{mercury::query::insert::values}"),
                'columns': re.compile(r"{mercury::query::insert::columns}"),
            },
            'identifier': re.compile(r"{mercury::query::identifier}"),
            'tables': re.compile(r"{mercury::query::tables}")
        },
    }

def transform(func, template=None):
    return FunctionTransformer(func).transform(template)

class FunctionTransformer:
    def __init__(self, Function, TabLevel = 1, TabWidth = 4):
        self.Function = Function
        self.Parameters = Function.Parameters
        self.Tables = Function.Tables
        self.DataRoot = Function.DataRoot
        self.Name = Function.Name
        self.Query = Function.Query
        self.TabLevel = TabLevel
        self.TabWidth = TabWidth
        
    def transform(self, template_content):
        return "\n".join([
            self._transform(line)
            for line in template_content.splitlines()
        ])
    
    def _transform(self, line):
        if "{mercury::imports}" in line:
            return "import " + '\nimport '.join((
                'json',
                're'
            ))
        elif match := expr['parameters']['declare'].search(line):
            return f'\n'.join([ParameterDeclaration(self.DataRoot, TabWidth=self.TabWidth, TabLevel=self.TabLevel).declare(p) for p in self.Function.Parameters])
        elif match := expr['parameters']['validate'].search(line):
            return f'\n'.join([ParameterValidation(TabWidth=self.TabWidth, TabLevel=self.TabLevel).validate(p) for p in self.Function.Parameters])
        elif match := expr['query']['declare'].search(line):
            return f'\n{' '*self.TabLevel * self.TabWidth}Query = f"""{QueryCreation(TabWidth=self.TabWidth, TabLevel=self.TabLevel).create(
                Query=self.Query,
                Parameters=self.Parameters,
                Tables=self.Tables
            )}"""'
        else: 
            return line
class ParameterDeclaration:

    def __init__(self, DataRoot, TabLevel=1, TabWidth=4):
        self.DataRoot = DataRoot
        self.TabWidth = TabWidth 
        self.TabLevel = TabLevel
    # Parameter Declaration
    def declare(self, Parameter: config_parser._Parameter):
        self.Parameter = Parameter
        return f'''{' '*self.TabWidth*self.TabLevel}{Parameter.Key} = {self.SourceToString(Parameter.Source)}'''
    def SourceToString(self, source: config_parser._Source):
        if source == None:
            return f'payload.{self.DataRoot}.{self.Parameter.Key}'
        if source.type == "URL":
            return self.URLSourceToString(source.source)
        if source.type == "Payload":
            return self.PayloadSourceToString(source.source)

    def PayloadSourceToString(self, Payload: config_parser._Payload):
        DataRoot = f'{self.DataRoot}.' if Payload.UseDataRoot else ""
        return f'''payload.{DataRoot}{Payload.Path}'''
    
    def URLSourceToString(self, URL:config_parser._URL):
        return f'''re.sub('{URL.Pattern}', r'{URL.Value}', payload.path)'''

class ParameterValidation:
    def __init__(self, TabLevel=1, TabWidth=4):
        self.content = ""
        self.TabLevel = TabLevel
        self.TabWidth = TabWidth
    def validate(self, Parameter: config_parser._Parameter):
        self.Parameter = Parameter 
        self.Name : str = self.Parameter.Key
        self.Type : config_parser._Type= self.Parameter.Type
        return self.validateType()
    def validateType(self):
        print('validating')
        if isinstance(self.Type.Type, config_parser._Integer):
            return self.validateInt()
        elif isinstance(self.Type.Type, config_parser._String):
            return self.validateString()
        else: return ""
    def fail(self, failure: config_parser._OnFail):
        return f'{' '*self.TabLevel*self.TabWidth}'\
            +'return {"statusCode": '\
            + str(failure.Code) \
            + ', "body": {"message": ' \
            + f'"{failure.Message}"' \
            + '}}'
    def validateInt(self):
        print(self.Type.Type.ValidationFail) 
        return f'\n{' '*self.TabWidth*self.TabLevel}' + f'\n{' '*self.TabWidth*self.TabLevel}'.join([
            f'try:',
            f'{' '*self.TabWidth*self.TabLevel}{self.Name} = int({self.Name})',
            f'except TypeError:',
            self.fail(self.Type.castFail),
            f'if not {self.Type.Type.Lower} < {self.Name} < {self.Type.Type.Upper}:',
            self.fail(self.Type.Type.ValidationFail),
        ])
    def validateString(self):
        print(self.Type.Type.LengthFail)
        return f"\n{' '*self.TabWidth*self.TabLevel}" + \
            f'\n{' '*self.TabWidth*self.TabLevel}'.join([
                f'if not {self.Type.Type.Lower} < len({self.Name}) < {self.Type.Type.Upper}:',
                self.fail(self.Type.Type.LengthFail),
                f'if not re.fullmatch(r"{self.Type.Type.Pattern}",{self.Name}):',
                self.fail(self.Type.Type.PatternFail)
            ])

class QueryCreation:
    def __init__(self, TabLevel, TabWidth):
        self.TabLevel = TabLevel
        self.TabWidth = TabWidth
    def create(self, Query, Tables, Parameters):
        self.Query: config_parser._Query = Query
        self.Table : config_parser._Table = Tables
        self.Parameters = Parameters
        return f""" {self.replacePlaceholders()} """
    def replacePlaceholders(self):
        query = self.Query.query
        query = expr['query']['select']['parameters'].sub(
            #f',\n{' '*self.TabLevel*self.TabWidth}'
            ' ,'.join([
            self.selectParameter(p)
            for p in self.Parameters]), query)
        query = expr['query']['update']['parameters'].sub(f',\n{' '*self.TabLevel*self.TabWidth}'.join([
            self.updateParameter(p)
            for p in self.Parameters if not p.Identifier]) + '\n', query)
        query = expr['query']['identifier'].sub(' AND '.join([
            self.identifier(p) for p in self.Parameters if p.Identifier
        ]), query)
        query = expr['query']['tables'].sub(self.tables(), query)
        columns, values = self.insert_tables()
        query = expr['query']['insert']['columns'].sub(columns, query)
        query = expr['query']['insert']['values'].sub(values, query)
        return query 

    def tables(self):
        return f'{self.Table.Name} {self.Table.Alias}'
        
    def updateParameter(self,p:config_parser._Parameter):
        print(p)
        return f'{self.Table.Alias}."{p.Column}" = ' + "{" + p.Key + '}'

    
    def selectParameter(self, p: config_parser._Parameter):
        return f' {self.Table.Alias}."{p.Column}"'

    def identifier(self, p: config_parser._Parameter):
        return f"{self.Table.Alias}.{p.Column} = " + "{" + p.Key + "}"
    
    def insert_tables(self):
        columns = []
        values = []
        def insert_table(param: config_parser._Parameter):
            return f'"{param.Column}"', '{' + param.Key + '}' 
        for p in self.Parameters:
            col, val = insert_table(p)
            columns.append(col)
            values.append(val)
        return f"{self.Table.Name}({','.join(columns)})", f"({','.join(values)})"

