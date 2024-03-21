


class _Table:
    def __init__(self, Key, Name, Alias, Default = False):
        print("mercury.config_parser - _Table.init() with: ", "\n  Key: ", Key, "\n  Name: ", Name, "\n  Alias: ", Alias, "\n  Default: ", Default)
        self.Key = Key
        self.Name = Name
        self.Alias = Alias
        self.Default = Default
    def __str__(self):
        return f"Table {self.Key}: {self.Name}, {self.Alias}, {self.Default}"
