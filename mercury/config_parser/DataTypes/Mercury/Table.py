

from mercury.logger.DebugLogger import DebugLogger

_logger = DebugLogger(__file__)


class _Table:
    def __init__(self, Key, Name, Alias, Default = False):
        _logger.log(msg="Initalizing", fname="_Table.init()",
                    kwargs={"Key":Key, "Name": Name, "Alias": Alias, "Default": Default})

        self.Key = Key
        self.Name = Name
        self.Alias = Alias
        self.Default = Default
    def __str__(self):
        return f"Table {self.Key}: {self.Name}, {self.Alias}, {self.Default}"
