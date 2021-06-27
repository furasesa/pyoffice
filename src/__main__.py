"""
pyoffice: combine sqlite3 and office
Usage:
pyoffice db [-v -p STORAGE -c CONFIG]

Options:
    -h --help       Show this screen
    -v --verbose    verbose
    -V --version    Print version
    -p DBPATH       Database Storage Path
    -c CONFIG       Path of pyoffice.ini [default: ./]
"""
import platform
from pathlib import Path
from docopt import docopt
import logging.config
import configparser

from .logging_config import LOG_CONFIG
from .app_config import config_validation

from .db.main import main

if __name__ == '__main__':
    args = docopt(__doc__, version='pyoffice 0.0.1')
    os = platform.system()
    # init class
    config = configparser.ConfigParser()
    # get docopt config
    is_verbose = args.get('--verbose')
    db_cli = args.get('db')
    defined_database_path = args.get('-p')
    defined_config_path = args.get('-c')

    # function of args
    verbosity = logging.DEBUG if is_verbose else logging.ERROR
    # update verbosity level in root config
    LOG_CONFIG.update({'root': {'handlers': ['console', 'filewritter'], 'level': logging.DEBUG}})
    logging.config.dictConfig(LOG_CONFIG)

    # for test only
    logging.info(args)

    # config validation
    config = config_validation(config, defined_database_path, defined_config_path)

    if os in config:
        logging.debug(config.sections())
        logging.info('done')
    else:
        logging.error('file config is empty. please use pyoffice db -p DBPATH')

    #
    # # if len(sys.argv) < 2:
    # #     db = ':memory:'
    # # else:
    # #     db = sys.argv[1]
    #
    # # main()
    #
    #

