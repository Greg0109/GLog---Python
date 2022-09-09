#!/usr/bin/env python3
"""This script handles the Pushover integration"""
import os
import requests

class Notifier():
    """This is the main class of the module"""
    def __init__(self, message):
        self.message = message

    def set_notifier(self):
        """This function sets the user, token and message"""
        return {
            'token': (None, os.getenv('PUSHOVER_TOKEN')),
            'user': (None, os.getenv('PUSHOVER_USER')),
            'message': (None, self.message)
        }

    def send_message(self):
        """This function sends the message"""
        return requests.post(
            'https://api.pushover.net/1/messages.json',
            files=self.set_notifier()
        )
