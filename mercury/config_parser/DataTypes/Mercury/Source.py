

from mercury.config_parser.DataTypes.Mercury.URL import _URL
from mercury.config_parser.DataTypes.Mercury.Payload import _Payload

from mercury.logger.DebugLogger import DebugLogger

_logger = DebugLogger(__file__)

class _Source():
    def __init__(self, source, source_defaults = ""): 
        _logger.log(msg="Initalizing", fname="_Source.init()",
                    kwargs={"source":source, "source_defaults": source_defaults})

        if 'URL' in source:
            self.type = "URL"
            self.source = _URL(**source['URL'])
        elif 'Payload' in source:
            self.type = "Payload"
            self.source = _Payload(**source['Payload'])

    def __str__(self):
        return f"Source: {self.type}, {str(self.source)} "
