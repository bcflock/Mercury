

from mercury.logger.DebugLogger import DebugLogger

_logger = DebugLogger(__file__)



class _Query:
    def __init__(self, Type="", Override=""):
        _logger.log(msg="Initalizing", fname="_Query.init()",kwargs={"Type":Type, "Override": Override})

        if not Type and not Override:
           raise ValueError 
        Type = Type.upper()
        if Type:
            if Type == "SELECT":
                self.query = '''
                    SELECT 
                        {mercury::query::select::parameters}
                    FROM 
                        {mercury::query::tables}
                    WHERE 
                        {mercury::query::identifier}
                    '''
            elif Type == "UPDATE":
                self.query = '''UPDATE 
                        {mercury::query::tables}
                    SET 
                        {mercury::query::update::parameters}
                    WHERE 
                        {mercury::query::identifier}
'''
            elif Type == "INSERT":
                self.query = '''
                    INSERT INTO 
                        {mercury::query::insert::columns}
                    VALUES 
                        {mercury::query::insert::values}
'''
            else:
                _logger.error(msg="Missing Query Type and no Override provided", fname="_Query.init()")
                raise("") # _logger.error() will output then raise the given message
        if Override:
            self.query = Override     
        if not self.query:
            _logger.error(msg="Missing Query Type and no Override provided", fname="_Query.init()")
            raise("") # _logger.error() will output then raise the given message


        
    def __str__(self):
        return f'Query: {self.query}'

