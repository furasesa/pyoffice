import logging

logger = logging.getLogger('appmain')

if __name__ == '__main__':
    # test logging
    logger.debug('main debug message %s' % (logging.DEBUG))
    logger.info('main info message %s' % (logging.INFO))
    logger.warning('main warn message %s' % (logging.WARNING))
    logger.error('main error message %s' % (logging.ERROR))
    logger.critical('main critical message %s' % (logging.CRITICAL))

