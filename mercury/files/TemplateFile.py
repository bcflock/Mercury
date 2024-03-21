
import pathlib
import re

import mercury.engines.engine as engine

from mercury.logger.DebugLogger import DebugLogger

_logger = DebugLogger(__file__)


class _TemplateFile:
    engine = None 
    filename = None
    extension = None
    content = None
    
    def __init__(self, fdir, filename):
        _logger.log(msg="Initalizing", fname="_TemplateFile.init()",kwargs={"fdir":fdir, "filename": filename})
        self.filename = filename 
        self.extension = pathlib.Path(filename).suffix
        self.engine = engine.get_engine_from_ext(self.extension)

        self.fdir = fdir
        with open(f'{self.fdir}/{self.filename}', 'r') as f:
            self.content = f.read()
        match = re.match(r'^(.*)\.mercury'+f'\\{self.extension}$', str(filename))
        self.outputname = match.group(1) + self.extension

    def __str__(self):
        return f"[{self.fdir}/{self.filename}, {self.extension}, {self.outputname}]"