import logging

from cryptocollector.cfg.config import DATE_FORMAT, LOG_FORMAT

def setup_logger(name, level=logging.INFO):        
    """

    Setup logging.

    Parameters
    ----------
    name : str
        Name of module.
    level : int
        Level of logging.

    """

    logger = logging.getLogger(name)
    logger.setLevel(level)    

    formatter = logging.Formatter(
        fmt=LOG_FORMAT,
        datefmt=DATE_FORMAT)

    sh = logging.StreamHandler()
    sh.setLevel(level)
    sh.setFormatter(formatter)

    logger.addHandler(sh)

    return logger