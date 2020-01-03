from configparser import ConfigParser
import os

ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
CONFIG_FILE = os.path.join(ROOT_DIR,'database.ini')

def db_config(schema, filename=CONFIG_FILE):
    parser = ConfigParser()
    parser.read(filename)
    db = {}
    if parser.has_section(schema):
        params = parser.items(section=schema)
        for param in params:
            db[param[0]] = param[1]
    else:
        print(parser)
        raise Exception('Section {0} not found in the file'.format(schema, filename))
    return db
    
# print(db_config('suppliers'))