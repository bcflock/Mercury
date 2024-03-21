import yaml
import pathlib
import enum
import re
import os
import mercury.engines.engine as engine

from mercury.files.MercuryFiles import _MercuryFiles
from mercury.files.TemplateFile import _TemplateFile
from mercury.files.StaticFile import _StaticFile

from mercury.config_parser.config_parser import ConfigParser


from mercury.logger.DebugLogger import DebugLogger

_logger = DebugLogger(__file__)


class Mercury():

    def __init__( self, config, templatedir, outputdir="output"):
        _logger.log(msg="Started", fname="Mercury.init()",kwargs={"config":config, "templatedir": templatedir})
        self.config = config
        self.templatedir = templatedir
        self.outputdir = outputdir

    def locate_files(self):
        p = pathlib.Path(f'./{self.templatedir}')
        static = []
        template = []
        walk = p.iterdir() 
        for file in walk:   
            _logger.log(msg="Processing File", fname="Mercury.locate_files()",kwargs={"file":file, "file.name": file.name})
            fpath = pathlib.Path(f'{file}')
            if str(fpath) == self.config: continue
            suff = fpath.suffixes
            if '.mercury' in suff:
                template.append(_TemplateFile(self.templatedir, file.name))
            else:
                static.append(_StaticFile(self.templatedir, file.name))
        _logger.log(msg="Finished", fname="Mercury.locate_files()",kwargs={"template":template, "static": static})

        return _MercuryFiles(template=template, static=static)
    
        # for fdir, subdir, files in walk:
        #     for file in files:
        #         fpath = pathlib.Path(f'{fdir}/{file}')
        #         if str(fpath) == self.config: continue
        #         suff = fpath.suffixes
        #         if '.mercury' in suff:
        #             template.append(_TemplateFile(fdir, file))
        #         else:
        #             static.append(_StaticFile(fdir, file))
        # return _MercuryFiles(template=template, static=static)
    
    def load_config(self):
        return ConfigParser.parse(self.config)
        


    def execute(self):
        self.locate_files().apply_config(
            self.load_config(),
            outputdir=self.outputdir
        )