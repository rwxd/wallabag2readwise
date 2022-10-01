import logging
from os import getenv

log_level = getenv('LOG_LEVEL', 'DEBUG')
logger = logging.getLogger('wallabag2readwise')

format = '%(levelname)s - %(asctime)s - %(name)s - %(message)s'
stream_handler = logging.StreamHandler()
stream_handler.setFormatter(logging.Formatter(format))
stream_handler.setLevel(log_level)

logger.addHandler(stream_handler)
logger.setLevel('DEBUG')
