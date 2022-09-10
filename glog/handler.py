#!/usr/bin/env python3
"""This is the main script of the module"""
import logging
import re
from glog.notifier import Notifier

def write(file, log):
    """Write logs to file"""
    with open(file, 'a+', encoding='utf-8') as file:
        file.write(log)


class GLogHandler(logging.StreamHandler):
    """This is the main class of the module"""
    def __init__(self, config_dict):
        super().__init__()
        self.parse_dict(config_dict)

    def parse_dict(self, config_dict):
        """This method is used to parse the config_dict"""
        self.send_to_pushover = config_dict.get('send_to_pushover', False)
        self.send_errors = config_dict.get('send_errors', False)
        self.write_to_file = config_dict.get('write_to_file', False)
        self.file_name = config_dict.get('file_name', 'glog.log')
        self.file_path = config_dict.get('file_path', '/tmp/logs/')
        self.pushover_token = config_dict.get('pushover_token', None)
        self.pushover_user = config_dict.get('pushover_user', None)

    def emit(self, record):
        try:
            msg = self.format(record)
            self.file_or_push(record, msg)
            stream = self.stream
            stream.write(msg)
            stream.write(self.terminator)
            self.flush()
        except (KeyboardInterrupt, SystemExit) as error:
            print(error)
            raise
        except Exception as _:  # pylint: disable=broad-except
            self.handleError(record)

    def file_or_push(self, record, msg):
        msg_no_colors = re.sub(r'\x1b\[([0-9]{1,2}(;[0-9]{1,2})?)?[m|K]', '', msg)
        logger_name = record.name
        if self.write_to_file:
            write('/var/log/{}.log'.format(logger_name), msg_no_colors)
        if self.send_to_pushover:
            message = f'{logger_name} {msg_no_colors}'
            Notifier(self.pushover_token, self.pushover_user, message)
        elif self.send_errors and (
            record.levelno == logging.ERROR or record.levelno == logging.WARNING
        ):
            message = f'{logger_name} {msg_no_colors}'
            Notifier(self.pushover_token, self.pushover_user, message)
