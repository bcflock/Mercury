



class _Query:
    def __init__(self, Type="", Override=""):
        print("mercury.config_parser - _Query.init() with: ", "\n  Type: ", Type, "\n  Override: ", Override)
        print("Type:",Type)
        print("Override:",Override)
        if not Type and not Override:
           raise ValueError 
        Type = Type.upper()
        if Type:
            print(Type)
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
                raise ValueError("Missing Query Type and no Override provided")
        if Override:
            self.query = Override     
        if not self.query:
            raise ValueError("Missing Query Type and no Override provided")

        
    def __str__(self):
        return f'Query: {self.query}'

