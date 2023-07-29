import logging

logger = logging.getLogger('wallabag2readwise')


def _setup_logging(verbose: bool, debug: bool):
    level = 'WARNING'
    if verbose:
        level = 'INFO'
    if debug:
        level = 'DEBUG'

    format = '%(levelname)s - %(asctime)s - %(name)s - %(message)s'

    stream_handler = logging.StreamHandler()
    stream_handler.setFormatter(logging.Formatter(format))
    stream_handler.setLevel(level)

    logger.addHandler(stream_handler)

    for handler in logging.root.handlers:
        handler.setLevel(level)
        handler.setFormatter(logging.Formatter(format))

    logging.basicConfig(format=format, level=level)

    logger.setLevel(level)
