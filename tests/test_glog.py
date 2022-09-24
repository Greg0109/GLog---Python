#!/usr/bin/env python

"""Tests for `glog` package."""

import pytest
import tempfile
from unittest.mock import patch
from glog import GLog


@pytest.fixture
def config_dict_no_pushover():
    """This fixture returns a config dict without pushover integratino"""
    return {
        'send_to_pushover': False,
    }


@pytest.fixture
def config_dict_pushover():
    """This fixture returns a config dict with pushover integration"""
    return {
        'send_to_pushover': True,
        'pushover_token': 'token',
        'pushover_user': 'user',
    }


@pytest.fixture
def config_dict_pushover_errors():
    """This fixture returns a config dict with pushover
    integration and only sends errors"""
    return {
        'send_to_pushover': True,
        'send_errors': True,
        'pushover_token': 'token',
        'pushover_user': 'user',
    }


@pytest.fixture
def config_dict_write_to_file():
    """This fixture returns a config dict with file integration"""
    tempfolder = tempfile.gettempdir()
    return {
        'write_to_file': True,
        'send_to_pushover': False,
        'file_path': str(tempfolder),
        'file_name': 'test.log',
    }


def test_log_something(config_dict_no_pushover, caplog):
    """This test logs something on the console"""
    glog = GLog('test', config_dict_no_pushover)
    glog.info('This is a test')
    assert 'This is a test' in caplog.text


def test_log_something_to_file(config_dict_write_to_file, caplog):
    """This test logs something to a file"""
    glog = GLog('test', config_dict_write_to_file)
    glog.info('This is a test')
    assert 'This is a test' in caplog.text
    with open(config_dict_write_to_file['file_path'] +
              config_dict_write_to_file['file_name']) as file:
        assert 'This is a test' in file.read()


def test_log_something_to_pushover(config_dict_pushover, caplog):
    """This test logs something to pushover"""
    with patch('requests.post') as mock_post:
        glog = GLog('test', config_dict_pushover)
        glog.info('This is a test')
        assert 'This is a test' in caplog.text
        mock_post.assert_called_with(
            'https://api.pushover.net/1/messages.json',
            files={
                'token': (None, 'token'),
                'user': (None, 'user'),
                'message': (None, '[test - info]  This is a test')
            },
            timeout=300
        )


def test_log_something_to_pushover_not_string(config_dict_pushover, caplog):
    """This test logs something to pushover"""
    with patch('requests.post') as mock_post:
        glog = GLog('test', config_dict_pushover)
        glog.info(123)
        assert '123' in caplog.text
        mock_post.assert_called_with(
            'https://api.pushover.net/1/messages.json',
            files={
                'token': (None, 'token'),
                'user': (None, 'user'),
                'message': (None, '[test - info]  123')
            },
            timeout=300
        )
