"""
pyoffice: combine sqlite3 and office
Usage:
pyoffice db gui [-v]
pyoffice db cli [-vCSQp WORKSPACE]

Options:
    -V          Print version
    -h --help   Show this screen
    -p PATH     Set Working Space [default: ./]
    -v          verbose
    -C          Sql cli command
    -S          Search Keywords
    -Q          Query table
"""
from pathlib import Path
from docopt import docopt
import logging.config
import configparser

from .logging_config import LOG_CONFIG
from .db.main import Database

# gui
from .ui.main import App


def main():
    args = docopt(__doc__, version='pyoffice 0.0.1')
    # os = platform.system()
    # init class
    config = configparser.ConfigParser()
    # get docopt config
    is_db = args.get('db')
    cli = args.get('cli')
    gui = args.get('gui')

    workspace = args.get('-p')
    is_verbose = args.get('-v')

    # Database Options
    db_cmd = args.get('-C')
    db_search = args.get('-S')
    db_query = args.get('-Q')

    # function of args
    verbosity = logging.DEBUG if is_verbose else logging.ERROR
    # print(f"verbosity : {verbosity} debug: {logging.DEBUG}\nis_verbose? {is_verbose}")
    # update verbosity level in root config
    LOG_CONFIG.update({'root': {'handlers': ['console', 'filewritter'], 'level': verbosity}})
    logging.config.dictConfig(LOG_CONFIG)

    # for test only
    logging.info(args)
    # print(args)

    # read workspace
    # looking for pyoffice.ini and pyoffice db
    workspace_path = Path(workspace)
    dbpath = workspace_path / 'pyoffice.db'
    cfgpath = workspace_path / 'pyoffice.ini'
    config.read(cfgpath)

    if gui:
        app = App(dbpath)
        app.mainloop()

    elif cli:
        # init class
        mdb = Database(dbpath)

        if db_cmd:
            mdb.cli()
        elif db_search:
            mdb.search(config)
        elif db_query:
            # Query
            filter_list = config['Query']['list'].split(',')
            query_dict = {}
            for x in filter_list:
                q_args = f"SELECT {config[x]['select']} FROM {config[x]['from']} "
                query_dict[x] = {}
                query_dict[x]['query'] = q_args
                # query_dict.update({x: {'query': q_args}})
                if 'column' in config[x]:
                    q_col = config[x]['column'].split(',')
                    query_dict[x]['column'] = q_col
                if 'filter' in config[x]:
                    q_filter = config[x]['filter'].split(',')
                    query_dict[x]['filter'] = q_filter

            logging.debug(f'dict to send: {query_dict}')
            mdb.query(query_dict)
    else:
        raise Exception("no gui nor db selected")


if __name__ == '__main__':
    main()

