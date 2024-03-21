


class _Payload():
    def __init__(self, Path, DataRoot=True):
        print("mercury.config_parser - _Payload.init() with: ", "\n  Path: ", Path, "\n  DataRoot: ", DataRoot)
        self.Path = Path
        self.UseDataRoot = DataRoot
        pass
    def __str__(self):
        return f'Payload: {self.Path}, {self.UseDataRoot}'

