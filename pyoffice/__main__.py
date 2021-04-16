import logging
from .db.connector import OfficeData

logger = logging.getLogger('main')

if __name__ == '__main__':
    data = OfficeData('db.json')

