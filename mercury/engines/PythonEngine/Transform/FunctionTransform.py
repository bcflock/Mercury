
from mercury.engines.PythonEngine.Transform.TransformConfig import expr
from mercury.engines.PythonEngine.Parameter.ParameterDeclaration import ParameterDeclaration
from mercury.engines.PythonEngine.Parameter.ParameterValidation import ParameterValidation
from mercury.engines.PythonEngine.Query.QueryCreation import QueryCreation

class FunctionTransformer:
    def __init__(self, Function, TabLevel = 1, TabWidth = 4):
        print("mercury.engines.PythonEngine - FunctionTransformer.init() with: ", "\n  Function: ", Function, "\n  TabLevel: ", TabLevel, "\n  TabWidth: ", TabWidth)
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
            return f'\n{" " * self.TabLevel * self.TabWidth}Query = f"""{QueryCreation(TabWidth=self.TabWidth, TabLevel=self.TabLevel).create(Query=self.Query,Parameters=self.Parameters,Tables=self.Tables)}"""'
        else: 
            return line