import re

expr = {
        'parameters': {
            'declare'  : re.compile(r"([\t\s]*){mercury::parameters::declare}"),
            'validate' : re.compile(r"([\t\s]*){mercury::parameters::validate}")
        },
        'query': {
            'declare': re.compile(r"([\t\s]*){mercury::query::declare}"),
            'select': {
                'parameters': re.compile(r"{mercury::query::select::parameters}")
            },
            'update': {
                'parameters': re.compile(r"{mercury::query::update::parameters}")
            },
            'insert': {
                'values': re.compile(r"{mercury::query::insert::values}"),
                'columns': re.compile(r"{mercury::query::insert::columns}"),
            },
            'identifier': re.compile(r"{mercury::query::identifier}"),
            'tables': re.compile(r"{mercury::query::tables}")
        },
    }
