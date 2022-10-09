#!/usr/bin/env python3
"""This script handles the Pushover integration"""
import requests
from pydantic import BaseModel, StrictStr, validator


class ConfigData(BaseModel):
    """This class holds the configuration data for the Pushover integration"""
    token: StrictStr
    user: StrictStr
    message: StrictStr

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


class Notifier():
    """This is the main class of the module"""

    def __init__(self, config_data):
        self.config_data = ConfigData(**config_data)
        self.send_message()

    def send_message(self):
        """This function sends the message"""
        try:
            requests.post(
                'https://api.pushover.net/1/messages.json',
                files={
                    'token': (None, self.config_data.token),
                    'user': (None, self.config_data.user),
                    'message': (None, self.config_data.message),
                },
                timeout=300
            )
        except requests.exceptions.RequestException as error:
            print(error)
