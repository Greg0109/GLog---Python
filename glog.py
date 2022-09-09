"""This is the main script of the project"""
import logging
import logging.handlers
from glog_handler import GLogHandler
import structlog


class GLog():
    """This is the main class of the project"""
    def __init__(self, logger_name, write_to_file=False, send_to_pushover=False):
        self.logger_name = logger_name
        self.write_to_file = write_to_file
        self.send_to_pushover = send_to_pushover
        self.logger = self.configure_logger()

    def configure_logger(self):
        """Configure python's standard logging"""
        logger = logging.getLogger(self.logger_name)
        logger.addHandler(GLogHandler(
            write_to_file=self.write_to_file,
            send_to_pushover=self.send_to_pushover
        ))
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
    