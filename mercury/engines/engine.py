import mercury.engines.PythonEngine

extension_map = {
    '.py': lambda : PythonEngine(),
    '.java': lambda : JavaEngine(),
    '.js': lambda : JSEngine(),
    '.ts': lambda : TSEngine(),
}
def get_engine_from_ext(ext):
    try:
        return extension_map[ext]()
    except NotImplementedError:
        raise NotImplementedError(f"Engine for {ext} files are not yet implemented")

class Engine:
    def __init__(self):
        raise NotImplementedError()
    def apply(self, template = None):
        raise NotImplementedError()

class PythonEngine(Engine):
    def __init__(self):
        pass
    def apply(self, model, template_content =""):
        return mercury.engines.PythonEngine.transform(model, template_content)

class JavaEngine(Engine):
    pass
class JSEngine(Engine):
    pass
class TSEngine(Engine):
    pass
class GoEngine(Engine):
    pass