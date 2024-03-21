

class _OnFail:
    def __init__(self, Code, Message = "", **kwargs):
        self.Code = Code or 400
        self.Message = Message or ""
    def __str__(self):
        return f'OnFail: {self.Code}, {self.Message}'
