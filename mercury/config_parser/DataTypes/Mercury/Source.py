

from mercury.config_parser.DataTypes.Mercury.URL import _URL
from mercury.config_parser.DataTypes.Mercury.Payload import _Payload

class _Source():
    def __init__(self, source, source_defaults = ""): 
        print("mercury.config_parser - _Source.init() with: ", "\n  source: ", source, "\n  source_defaults: ", source_defaults)
        if 'URL' in source:
            self.type = "URL"
            self.source = _URL(**source['URL'])
        elif 'Payload' in source:
            self.type = "Payload"
            self.source = _Payload(**source['Payload'])

    def __str__(self):
        return f"Source: {self.type}, {str(self.source)} "
