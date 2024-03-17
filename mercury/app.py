import yaml
import pathlib
import enum
import re
import os
import mercury.engines.engine as engine
from . import config_parser
class _TemplateFile:
    engine = None 
    filename = None
    extension = None
    content = None
    
    def __init__(self, fdir, filename):
        self.filename = filename 
        self.extension = pathlib.Path(filename).suffix
        self.engine = engine.get_engine_from_ext(self.extension)

        self.fdir = fdir
    #    print(f'File extension = {self.extension}')
    #    print(f'Dir = {self.fdir}')
        with open(f'{self.fdir}/{self.filename}', 'r') as f:
            self.content = f.read()
        match = re.match(r'^(.*)\.mercury'+f'\\{self.extension}$', str(filename))
        self.outputname = match.group(1) + self.extension

    def __str__(self):
        return f"[{self.fdir}/{self.filename}, {self.extension}, {self.outputname}]"
class _StaticFile:
    def __init__(self, fdir, filename):
        self.fdir = fdir
        self.filename = filename
        with open(f'{self.fdir}/{self.filename}', 'r') as f:
            self.content = f.read()
    def write(self, fname):
        with open(f'{fname}/{self.filename}', 'w+') as f:
            f.write(self.content)

class _MercuryFiles:

    def __init__(self, static, template):
        self.static_files = static 
        self.template_files = template

    def apply_config(self, model: config_parser.Model):
        """_summary_
            creates the folders for each of the functions,
            copies over static files and applies config
        Args:
            config (_type_): _description_
            """
        #print(model)
        
        #folders = [f.Name for f in model.Functions]
        folders = ['test']
        for fname in folders:
            os.makedirs(f'./{fname}', exist_ok=True )
            for template in self.template_files:
                with open(f'{fname}/{template.outputname}', 'w+') as f:
                    f.writelines(template.engine.apply(model, template.content))
                    #f.write(template.engine.apply(model))
            for static in self.static_files:
                with open(f'{fname}/{static.filename}', 'w+') as f:
                    static.write(fname)

class Mercury():

    def __init__( self, config, templatedir ):
        self.config = config
        self.templatedir = templatedir

    def locate_files(self):
        p = pathlib.Path(f'./{self.templatedir}')
        files = p.walk() 
        static = []
        template = []
        walk = p.walk() 

        for fdir, subdir, files in walk:
            for file in files:
                fpath = pathlib.Path(f'{fdir}/{file}')
                if str(fpath) == self.config: continue
                suff = fpath.suffixes
                if '.mercury' in suff:
                    template.append(_TemplateFile(fdir, file))
                else:
                    static.append(_StaticFile(fdir, file))
        return _MercuryFiles(template=template, static=static)
    
    def load_config(self):
        return config_parser.ConfigParser.parse(self.config)
        


    def execute(self):
        self.locate_files().apply_config(
            self.load_config()
        )