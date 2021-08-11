import platform
import logging
from pathlib import Path


def config_validation(cfg, defined_database_path, defined_config_path):
    os = platform.system()
    if defined_database_path:
        # read config in default and replace new database path
        logging.info('defined database path: {}'.format(defined_database_path))
        config_path = Path(defined_config_path)
        db_path = Path(defined_database_path)
        config_file = config_path / 'pyoffice.ini'
        logging.info('use config path: {}'.format(config_path))
        logging.info('use database path: {}'.format(db_path))
        # replace default storage location
        cfg[os] = {'dbpath': defined_database_path}
        with open(str(config_file), 'w') as configfile:
            cfg.write(configfile)
    else:
        # read config
        config_path = Path(defined_config_path)
        config_file = config_path / 'pyoffice.ini'
        logging.info('use config path: {}'.format(config_path))
        cfg.read(config_file)

    return cfg
