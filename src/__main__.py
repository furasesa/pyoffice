"""
pyoffice: combine sqlite3 and office
Usage:
pyoffice -V
pyoffice db [-vp DBPATH]
pyoffice db [-vc CONFIG] (--cli | --search)

Arguments:
    db              Run Database

Options:
    -h --help       Show this screen
    -v --verbose    verbose
    -V --version    Print version
    -p DBPATH       Set Database Storage Path and exit
    -c CONFIG       Path of pyoffice.ini [default: ./]

DbOpts:
    --cli           Sql cli command
    --search        Search Keywords

"""
import platform
from pathlib import Path
from docopt import docopt
import logging.config
import configparser

from .logging_config import LOG_CONFIG
from .app_config import config_validation

from .db.main import Database

if __name__ == '__main__':
    args = docopt(__doc__, version='pyoffice 0.0.1')
    os = platform.system()
    # init class
    config = configparser.ConfigParser()
    # get docopt config
    is_verbose = args.get('--verbose')
    db = args.get('db')
    defined_database_path = args.get('-p')
    defined_config_path = args.get('-c')

    # Database Options
    db_cli = args.get('--cli')
    db_search = args.get('--search')

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
        logging.debug(f'read sections: {config.sections()}')
        logging.info(f'os info: {os}')

    else:
        logging.error('file config is empty. please use pyoffice db -p DBPATH')

    dbpath = Path(str(config[os]['dbpath']))
    db_file = dbpath / 'pyoffice.db'
    logging.info(f'load : {db_file}, type: {type(db_file)}')

    # init class
    mdb = Database(db_file)

    if db and db_cli:
        mdb.cli()
    elif db and db_search:
        mdb.search()
