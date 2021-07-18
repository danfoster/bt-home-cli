import logging
import logging.handlers

logger = logging.getLogger(__name__.split('.')[0])

def setup_logging(syslog=False, debug=False):
    '''
    Configures logging
    '''
    # logger.propagate = False
    print(logger.name)
    formatter = logging.Formatter('[%(levelname)s] %(asctime)s - %(message)s')
    if debug:
        logger.setLevel(logging.DEBUG)
        logger.debug("Set log level to debug")
    else:
        logger.setLevel(logging.INFO)
    streamh = logging.StreamHandler()
    streamh.setFormatter(formatter)
    logger.addHandler(streamh)
    if syslog:
        syslogh = logging.handlers.SysLogHandler(address='/dev/log')
        syslogh.setFormatter(formatter)
        logger.addHandler(syslogh)