from os import path
import logging
import logging.config

# load config
log_file_path = path.join(path.dirname(path.abspath(__file__)), 'logger.conf')
logging.config.fileConfig(log_file_path, disable_existing_loggers=False, )

# create logger
logger = logging.getLogger(__name__)
# dbslog = logging.getLogger('dbs')

# test logging
logger.debug('init debug message %s' % (logging.DEBUG))
logger.info('init info message %s' % (logging.INFO))
logger.warning('init warn message %s' % (logging.WARNING))
logger.error('init error message %s' % (logging.ERROR))
logger.critical('init critical message %s' % (logging.CRITICAL))

# dbslog.debug('dbslog debug message %s' % (logging.DEBUG))
# dbslog.info('dbslog info message %s' % (logging.INFO))
# dbslog.warning('dbslog warn message %s' % (logging.WARNING))
# dbslog.error('dbslog error message %s' % (logging.ERROR))
# dbslog.critical('dbslog critical message %s' % (logging.CRITICAL))