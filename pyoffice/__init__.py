from os import path
import logging
import logging.config

# load config
log_file_path = path.join(path.dirname(path.abspath(__file__)), 'logger.conf')
logging.config.fileConfig(log_file_path, disable_existing_loggers=False )

# create logger
logger = logging.getLogger(__name__)
