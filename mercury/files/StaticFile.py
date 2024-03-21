



class _StaticFile:
    def __init__(self, fdir, filename):
        print("mercury.app - _StaticFile.init() with: ", "\n  fdir: ", fdir, "\n  filename: ", filename)
        self.fdir = fdir
        self.filename = filename
        with open(f'{self.fdir}/{self.filename}', 'r') as f:
            self.content = f.read()
    def write(self, fname):
        with open(f'{fname}/{self.filename}', 'w+') as f:
            f.write(self.content)
