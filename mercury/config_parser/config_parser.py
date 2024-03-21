import yaml

from mercury.config_parser.DataTypes.Model import Model


#TODO: There should be a refactor that takes advantage of yaml tags for directly creating the objects

class ConfigParser:
    def parse(config):
        with open(config, 'r') as f:
            inputstring = f.read()
            model = Model(**yaml.safe_load( inputstring )) 
        return model

