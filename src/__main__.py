"""
pyoffice: combine sqlite3 and office
Usage:  pyoffice -h
        pyoffice --version
        pyoffice [-vtp] [--gui]

Options:
    -h --help       Show this screen
    -v --verbose    verbose
    -V --version    Print version
    --gui           run gui (future)
    -t              is test
    -p              another test
"""

from docopt import docopt
import logging.config
from .logging_config import root_config, LOG_CONFIG

# log = logging.getLogger('__main__')

if __name__ == '__main__':
    args = docopt(__doc__, version='pyoffice 0.0.1')
    # get docopt config
    is_verbose = args.get('--verbose')
    is_gui = args.get('--gui')
    is_t = args.get('-t')
    is_p = args.get('-p')

    # function of args
    verbosity = logging.DEBUG if is_verbose else logging.ERROR

    # for test only
    print(args)
    print('is verbose:', verbosity)
    print('is test: ', is_t)
    print('is p: ', is_p)

    # update verbosity level in root config
    root_config.update({'root': {'handlers': ['console', 'filewritter'], 'level': verbosity}})

    # insert all config to logging_config
    LOG_CONFIG.update(root_config)
    print(LOG_CONFIG)

    logging.config.dictConfig(LOG_CONFIG)
    # test debug config

    logging.debug('debug')
    logging.info('info')
    logging.warning('warning')
    logging.error('error')
    logging.critical('critical')


