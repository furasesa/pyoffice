import logging
from tinydb import TinyDB, Query, storages
from tinydb.storages import JSONStorage
from tinydb_serialization import SerializationMiddleware
from tinydb_serialization.serializers import DateTimeSerializer
from datetime import datetime
from cryptography.fernet import Fernet
from pathlib import Path

log = logging.getLogger('database')

def generate_key():
    """
    Generates a key and save it into a file
    """
    key = Fernet.generate_key()
    with open("secret.key", "wb") as key_file:
        key_file.write(key)

def load_key():
    """
    Loads the key named `secret.key` from the current directory.
    """
    return open("secret.key", "rb").read()

class OfficeData:
    def __init__(self, dbfolder, username, passwd):
        serialization = SerializationMiddleware(JSONStorage)
        serialization.register_serializer(DateTimeSerializer(), 'TinyDate')

        self.path_db = Path(dbfolder / 'db.json')
        self.path_setting = Path(dbfolder / 'setting.json')
        
        self.db = TinyDB(self.path_db, storage=serialization)
        self.setting = TinyDB(self.path_setting, storage=serialization)
        self.user = username
        self.passwd = passwd

        # perform loggin
    
    def test_save_setting(self):
        log.debug('performing login test')
        id_test = self.setting.table('test')
        id_test.truncate()
        id_test.insert_multiple([
            {'login': {'date': datetime.now(), 'name': self.user, 'passwd': self.passwd}},
            {'app': {'path_db': str(self.path_db), 'path_setting': str(self.path_setting)}}
        ])
        log.debug(id_test.all())

    def test(self):
        log.debug('performing test data. create table test')
        log.info(self.db.tables())
        test_db = self.db.table('test')
        log.debug('erase all record in test table') #test only
        test_db.truncate()

        log.info('test insert some tables')
        # user_table = test.db.table('users')
        # self.product_table = self.db.table('products')
        test_db.insert_multiple([
            {'name': 'furasesa', 'role': 0},
            {'name': 'admin', 'role': 1},
            {'name': 'personalia', 'role': 2},
            {'name': 'dbmanager', 'role': 3},
            {'name': 'dbrecorder', 'role': 4},
            {'name': 'ordinary', 'role': 5}
        ])
        
        test_db.insert_multiple([
            {'pid': 'LA250', 'name': 'Pressure Gauge 250 bar', 'buy_price': 140000, 'buy_date': 14042020},
            {'pid': 'MF12', 'name': 'Filter Oli 1-1/2', 'buy_price': 75000, 'buy_date': 14052020},
        ])
        log.debug(test_db.all())

        log.info('all database insert done')
        # for user in self.user_table:
        #     print(user)
        for item in test_db:
            print(item)


        




# db = TinyDB('db.json')
# User = Query()
# db.insert({'name': 'John', 'age': 22})
# db.search(User.name == 'John')