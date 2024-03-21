

from mercury.config_parser.Handlers.OnFail import _OnFail
from mercury.config_parser.PatternsConfig import Patterns


class _String:
    def __init__(self, Pattern=None, Length={}, **kwargs):
        self.Lower = Length.get('Lower', 0)
        self.Upper = Length.get('Upper', "float('inf')")
        self.LengthFail = _OnFail(**Length.get('OnFail', {"Code": 400}))
        if Pattern:
            if isinstance(Pattern, str):
                if Pattern in Patterns.keys():
                    self.Pattern = Patterns.get(Pattern)
                else:
                    raise ValueError("Arbitrary Regular Expressions must be in an Expression tag")
                self.PatternFail = _OnFail(Code=400)
            else:
                self.Pattern = Pattern.get("Expression", r"/.*/") or r"/.*/"
                if self.Pattern.startswith('/') and self.Pattern.endswith('/'):
                    self.Pattern = self.Pattern[1:-1]
                else:
                    raise ValueError('Expressions should be formatted using this notation: //')
                self.PatternFail = _OnFail(**Pattern.get("OnFail", {'Code': 400}))
        else: 
            self.Pattern = r'.*'
            self.PatternFail = _OnFail(400)

    def __str__(self):
        return f'({type(self).__name__}: Pattern: /{self.Pattern}/, Length:[{self.Lower}, {self.Upper}])'
