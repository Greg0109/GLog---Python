#!/usr/bin/env python3
"""This script handles the Pushover integration"""
import requests
import json
import os
from pydantic import BaseModel, StrictStr, validator


class ConfigData(BaseModel):
    """This class holds the configuration data for the Pushover integration"""
    message: StrictStr
    service: StrictStr = 'ntfy'
    ntfy_host: StrictStr = 'https://ntfy.sh'

    @validator('message')
    def reformat_message(cls, value):
        """
        This is the normal format for the message
        logname date time [level  ] message

        This function replaces that format with
        [logname - level] message
        """
        value = value.split(' ')
        logname = value[0]
        level = value[3].replace('[', '')
        message = ' '.join(value[4:])
        return_message = f'[{logname} - {level}] {message}'
        return_message = return_message.replace('    ]', '').replace('  ]', '')
        return return_message
    
    @validator('service')
    def check_service(cls, value):
        """
        This function checks that the service is either ntfy or ntfy
        """
        if value not in ['ntfy', 'ntfy']:
            raise ValueError('service must be either ntfy or ntfy')
        return value


class Notifier():
    """This is the main class of the module"""

    def __init__(self, config_data):
        self.config_data = ConfigData(**config_data)
        if self.config_data.service == 'ntfy':
            self.send_ntfy_message()
        else:
            raise ValueError('service must be either ntfy or ntfy')

    def send_ntfy_message(self):
        """This function sends the message via ntfy"""
        try:
            response = requests.put(
                url = self.config_data.ntfy_host,
                data = self.config_data.message
            )
        except requests.exceptions.RequestException as error:
            print(error)