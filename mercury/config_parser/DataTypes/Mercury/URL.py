
class _URL():
    def __init__(self, Pattern, Value):
        print("mercury.config_parser - _URL.init() with: ", "\n  Pattern: ", Pattern, "\n  Value: ", Value)
        self.Pattern = Pattern
        self.Value = Value
        pass
    def __str__(self):
        return 'URL: {self.Pattern}, {self.Value}'
        
    