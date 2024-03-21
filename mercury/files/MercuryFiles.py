import os

from mercury.config_parser.DataTypes.Model import Model

from mercury.logger.DebugLogger import DebugLogger

_logger = DebugLogger(__file__)


class _MercuryFiles:

    def __init__(self, static, template):
        self.static_files = static 
        self.template_files = template

    def apply_config(self, model: Model, outputdir="output"):
        """_summary_
            creates the folders for each of the functions,
            copies over static files and applies config
        Args:
            config (_type_): _description_
            """
        _logger.log(msg="Apply Config", 
                    fname="_MercuryFiles.apply_config()",
                    kwargs={"model": model})
        #folders = [f.Name for f in model.Functions]
        os.makedirs(f'./{outputdir}', exist_ok=True )
        for func in model.Functions:
            fname = func.Name
            os.makedirs(f'./{outputdir}/{fname}', exist_ok=True )
            for template in self.template_files:
                with open(f'{outputdir}/{fname}/{template.outputname}', 'w+') as f:
                    f.write(template.engine.apply(func, template.content))
                    #f.write(template.engine.apply(model))
            for static in self.static_files:
                with open(f'{outputdir}/{fname}/{static.filename}', 'w+') as f:
                    static.write(fname)

            _logger.log(msg="Finished Function", 
                        fname="_MercuryFiles.apply_config()",
                        kwargs={"func": func})
            