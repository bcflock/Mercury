

from mercury.config_parser.DataTypes.Types import _Parameter, _Query, _Table

from mercury.engines.PythonEngine.Transform.TransformConfig import expr

class QueryCreation:
    def __init__(self, TabLevel, TabWidth):
        print("mercury.engines.PythonEngine - QueryCreation.init() with: ", "\n  TabLevel: ", TabLevel, "\n  TabWidth: ", TabWidth)
        self.TabLevel = TabLevel
        self.TabWidth = TabWidth
    def create(self, Query, Tables, Parameters):
        self.Query: _Query = Query
        self.Table : _Table = Tables
        self.Parameters = Parameters
        return f""" {self.replacePlaceholders()} """
    def replacePlaceholders(self):
        query = self.Query.query
        query = expr['query']['select']['parameters'].sub(
            #f',\n{" "*self.TabLevel*self.TabWidth}'
            ' ,'.join([
            self.selectParameter(p)
            for p in self.Parameters]), query)
        query = expr['query']['update']['parameters'].sub(f',\n{" "*self.TabLevel*self.TabWidth}'.join([
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
        
    def updateParameter(self,p:_Parameter):
        return f'{self.Table.Alias}."{p.Column}" = ' + "{" + p.Key + '}'

    
    def selectParameter(self, p: _Parameter):
        return f' {self.Table.Alias}."{p.Column}"'

    def identifier(self, p: _Parameter):
        return f"{self.Table.Alias}.{p.Column} = " + "{" + p.Key + "}"
    
    def insert_tables(self):
        columns = []
        values = []
        def insert_table(param: _Parameter):
            return f'"{param.Column}"', '{' + param.Key + '}' 
        for p in self.Parameters:
            col, val = insert_table(p)
            columns.append(col)
            values.append(val)
        return f"({','.join(columns)})", f"({','.join(values)})"
