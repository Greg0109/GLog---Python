#!/usr/bin/env python3
"""This script handles the Pushover integration"""
import requests
from pydantic import BaseModel, StrictStr, validator


class ConfigData(BaseModel):
    """This class holds the configuration data for the Pushover integration"""
    api_token: StrictStr
    user_key: StrictStr
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
        level = value[3].replace('[', '').replace(']', '')
        message = ' '.join(value[9:])
        return f'[{logname} - {level}] {message}'


class Notifier():
    """This is the main class of the module"""

    def __init__(self, pushover_token, pushover_user, message):
        self.config_data = ConfigData(
            api_token=pushover_token,
            user_key=pushover_user,
            message=message
        )
        self.send_message()

    def send_message(self):
        """This function sends the message"""
        requests.post(
            'https://api.pushover.net/1/messages.json',
            files=self.config_data.json(),
            timeout=300
        )
