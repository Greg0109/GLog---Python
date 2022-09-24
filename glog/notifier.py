#!/usr/bin/env python3
"""This script handles the Pushover integration"""
import requests


class Notifier():
    """This is the main class of the module"""

    def __init__(self, pushover_token, pushover_user, message):
        self.config_data = {
            'token': (None, pushover_token),
            'user': (None, pushover_user),
            'message': (None, message),
        }
        self.send_message()

    def send_message(self):
        """This function sends the message"""
        requests.post(
            'https://api.pushover.net/1/messages.json',
            files=self.config_data,
            timeout=300
        )
