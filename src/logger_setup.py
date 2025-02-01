'''
https://github.com/rajansahu713/FastAPI-Projects/tree/main/FastAPI%20with%20Python%20Logging
'''
import os
import logging
from logging.handlers import TimedRotatingFileHandler

import src.config as cfg


# Custom filter to filter log records based on severity level
class SeverityFilter(logging.Filter):
    def __init__(self, severity):
        super().__init__()
        self.severity = severity

    def filter(self, record):
        return record.levelno == self.severity


# Set up logging
levels = {
    'DEBUG': logging.DEBUG,
    'INFO': logging.INFO,
    'WARNING': logging.WARNING,
    'ERROR': logging.ERROR
}
level = levels.get(cfg.logs_level, logging.NOTSET)
logging.basicConfig(level=level)

# Create a formatter
formatter = \
    logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")

logs_root = cfg.logs_root


# Create a handler
def get_handler(path, level, logging_level, formatter):
    if not os.path.exists(path):
        os.makedirs(path)
    filename = f"{path}/{level}.log"
    handler = TimedRotatingFileHandler(filename, "midnight", backupCount=7)
    handler.setLevel(logging_level)
    handler.setFormatter(formatter)
    handler.addFilter(SeverityFilter(logging_level))
    return handler


# Create a logger
def get_logger(name=__name__):
    logger = logging.getLogger(name)

    log_file = f"{logs_root}/info"
    hnd = get_handler(log_file, "info", logging.INFO, formatter)
    logger.addHandler(hnd)

    log_file = f"{logs_root}/warning"
    hnd = get_handler(log_file, "warning", logging.WARNING, formatter)
    logger.addHandler(hnd)

    log_file = f"{logs_root}/error"
    hnd = get_handler(log_file, "error", logging.ERROR, formatter)
    logger.addHandler(hnd)
    return logger
