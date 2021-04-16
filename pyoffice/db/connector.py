import logging
from tinydb import TinyDB, Query

log = logging.getLogger('database')

class OfficeData:
    def __init__(self, jsondb):
        self.db = TinyDB(jsondb)
        log.debug('load database %s' %jsondb)
        log.debug('erase all record') #test only
        self.db.truncate()
        log.info('test insert some tables')
        self.user_table = self.db.table('users')
        self.product_table = self.db.table('products')
        self.user_table.insert_multiple([
            {'name': 'furasesa', 'role': 0},
            {'name': 'admin', 'role': 1},
            {'name': 'personalia', 'role': 2},
            {'name': 'dbmanager', 'role': 3},
            {'name': 'dbrecorder', 'role': 4},
            {'name': 'ordinary', 'role': 5}
        ])
        
        self.product_table.insert_multiple([
            {'pid': 'LA250', 'name': 'Pressure Gauge 250 bar', 'buy_price': 140000, 'buy_date': 14042020},
            {'pid': 'MF12', 'name': 'Filter Oli 1-1/2', 'buy_price': 75000, 'buy_date': 14052020},
        ])
        log.debug(self.user_table.all())
        log.debug(self.product_table.all())

        log.info('all database insert done')
        for user in self.user_table:
            print(user)
        for product in self.product_table:
            print(product)
        



        

# db = TinyDB('db.json')
# User = Query()
# db.insert({'name': 'John', 'age': 22})
# db.search(User.name == 'John')