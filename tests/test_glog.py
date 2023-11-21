#!/usr/bin/env python

"""Tests for `glog` package."""

import pytest
import tempfile
from unittest.mock import patch
from glog import GLog


@pytest.fixture
def config_dict_no_ntfy():
    """This fixture returns a config dict without ntfy integratino"""
    return {
        'send_to_ntfy': False,
    }


@pytest.fixture
def config_dict_ntfy():
    """This fixture returns a config dict with ntfy integration"""
    return {
        'send_to_ntfy': True,
    }


@pytest.fixture
def config_dict_ntfy_errors():
    """This fixture returns a config dict with ntfy
    integration and only sends errors"""
    return {
        'send_to_ntfy': True,
        'send_errors': True,
    }


@pytest.fixture
def config_dict_write_to_file():
    """This fixture returns a config dict with file integration"""
    tempfolder = tempfile.gettempdir()
    return {
        'write_to_file': True,
        'send_to_ntfy': False,
        'file_path': str(tempfolder),
        'file_name': 'test.log',
    }


def test_log_something(config_dict_no_ntfy, caplog):
    """This test logs something on the console"""
    glog = GLog('test', config_dict_no_ntfy)
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


def test_log_something_to_ntfy(config_dict_ntfy, caplog):
    """This test logs something to ntfy"""
    with patch('requests.post') as mock_post:
        glog = GLog('test', config_dict_ntfy)
        glog.info('This is a test')
        assert 'This is a test' in caplog.text
        mock_post.assert_called_with(
            'https://api.ntfy.net/1/messages.json',
            files={
                'message': (None, '[test - info]  This is a test')
            },
            timeout=300
        )


def test_log_something_to_ntfy_not_string(config_dict_ntfy, caplog):
    """This test logs something to ntfy"""
    with patch('requests.post') as mock_post:
        glog = GLog('test', config_dict_ntfy)
        glog.info(123)
        assert '123' in caplog.text
        mock_post.assert_called_with(
            'https://api.ntfy.net/1/messages.json',
            files={
                'message': (None, '[test - info]  123')
            },
            timeout=300
        )
