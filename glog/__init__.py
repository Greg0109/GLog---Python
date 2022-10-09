"""This is the main script of the project"""
import logging
import logging.handlers
from glog.handler import GLogHandler
import structlog

__author__ = """Greg Rabago"""
__email__ = 'greg.rabago@gmail.com'
__version__ = '1.0.1'


class GLog():
    """This is the main class of the project"""
    def __init__(self, logger_name, config_dict):
        self.logger_name = logger_name
        self.config_dict = config_dict
        self.logger = self.configure_logger()

    def configure_logger(self):
        """Configure python's standard logging"""
        logger = logging.getLogger(self.logger_name)
        logger.addHandler(GLogHandler(self.config_dict))
        logger.level = logging.DEBUG
        return structlog.wrap_logger(logger)

    def info(self, msg):
        """Log info messages"""
        self.logger.info(msg)

    def warning(self, msg):
        """Log warning messages"""
        self.logger.warning(msg)

    def error(self, msg):
        """Log error messages"""
        self.logger.error(msg)
