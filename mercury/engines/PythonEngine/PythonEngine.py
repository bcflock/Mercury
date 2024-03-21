from mercury.engines.PythonEngine.Transform.FunctionTransform import FunctionTransformer 



#TODO: This is not a real solution
def transform(func, template=None):
    return FunctionTransformer(func).transform(template)
