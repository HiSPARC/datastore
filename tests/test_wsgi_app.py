"""Acceptance tests for the datastore WSGI app"""

import functools
import hashlib
import pickle
import unittest

from http import HTTPStatus
from pathlib import Path
from unittest import mock

from webtest import TestApp

from wsgi import wsgi_app

self_path = Path(__file__).parent
test_data_path = self_path / 'test_data'

# configuration:
DATASTORE_PATH = self_path / 'fake_datastore'
CONFIGFILE = test_data_path / 'config.ini'

STATION_ID = 99
PASSWORD = 'fake_station'

EVENTPY2 = test_data_path / 'incoming_http/py2_s510_100events'
EVENTPY3 = test_data_path / 'incoming_http/py3event'
EVENTSUS = test_data_path / 'incoming_http/suspicious_event'


def configure_wsgi_app():
    """import the WSGI application"""

    return functools.partial(wsgi_app.application, configfile=CONFIGFILE)


def get_wsgi_app(wsgi_app=None):
    """return the WSGI application"""
    if wsgi_app is None:
        wsgi_app = configure_wsgi_app()
    return wsgi_app


@mock.patch('wsgi.wsgi_app.MINIMUM_YEAR', 2016)
class TestWsgiAppAcceptance(unittest.TestCase):
    def setUp(self):
        self.station_id = STATION_ID
        self.password = PASSWORD
        self.app = TestApp(get_wsgi_app())

    def tearDown(self):
        self.clean_datastore()

    def test_invalid_post_data(self):
        resp = self.app.post('/', {})
        self.assertEqual(resp.body, b'400')  # invalid post data
        self.assertEqual(resp.status_code, HTTPStatus.OK)
        self.assert_num_files_in_datastore(incoming=0, suspicious=0)

    def test_unpickling_error(self):
        broken_pickle = b'aaaaa'
        resp = self.upload(broken_pickle)
        self.assertEqual(resp, b'208')  # unpickle error
        self.assert_num_files_in_datastore(incoming=0, suspicious=0)

    def test_invalid_checksum(self):
        event_list = self.read_pickle(EVENTPY2)
        resp = self.upload(event_list, checksum=b'invalid')
        self.assertEqual(resp, b'201')  # input error
        self.assert_num_files_in_datastore(incoming=0, suspicious=0)

    def test_invalid_station_id(self):
        event_list = self.read_pickle(EVENTPY2)
        self.station_id = 0  # invalid station
        resp = self.upload(event_list)
        self.assertEqual(resp, b'206')  # invalid station id
        self.assert_num_files_in_datastore(incoming=0, suspicious=0)

    def test_invalid_password(self):
        event_list = self.read_pickle(EVENTPY2)
        self.password = 'wrong_password'
        resp = self.upload(event_list)
        self.assertEqual(resp, b'203')  # wrong password
        self.assert_num_files_in_datastore(incoming=0, suspicious=0)

    def test_put_py2_event(self):
        event_list = self.read_pickle(EVENTPY2)
        # Make sure the eventlist is indeed pickled on Python 2
        with self.assertRaises(UnicodeDecodeError):
            pickle.loads(event_list)

        resp = self.upload(event_list)
        self.assertEqual(resp, b'100')
        self.assert_num_files_in_datastore(incoming=1)
        self.assert_num_events_written(100)

    def test_put_py3_event(self):
        event_list = self.read_pickle(EVENTPY3)
        # Make sure the python 3 pickle is indeed pickled on Python 3
        try:
            pickle.loads(event_list)
        except UnicodeDecodeError:
            self.fail('Data does not seem pickled on python 3')

        resp = self.upload(event_list)
        self.assertEqual(resp, b'100')
        self.assert_num_files_in_datastore(incoming=1)
        self.assert_num_events_written(1)

    def test_put_suspicious_event(self):
        event_list = self.read_pickle(EVENTSUS)
        resp = self.upload(event_list)
        self.assertEqual(resp, b'100')
        self.assert_num_files_in_datastore(suspicious=1)

    def upload(self, pickled_data, checksum=None):
        """POST. Return response"""

        if checksum is None:
            checksum = hashlib.md5(pickled_data).hexdigest()

        data = {
            'station_id': self.station_id,
            'password': self.password,
            'data': pickled_data.decode('latin-1'),
            'checksum': checksum,
        }

        response = self.app.post('/', data)
        self.assertEqual(response.status_code, HTTPStatus.OK)
        return response.body

    def read_pickle(self, fn):
        event = fn.read_bytes()
        return event

    def files_in_folder(self, path):
        return [file for file in path.iterdir() if file.name != '.keep']

    def clean_datastore(self):
        for folder in ['incoming', 'tmp', 'suspicious', 'logs']:
            for filepath in self.files_in_folder(DATASTORE_PATH / folder):
                filepath.unlink()

    def assert_num_files_in_datastore(self, incoming=0, suspicious=0):
        self.assertEqual(len(self.files_in_folder(DATASTORE_PATH / 'tmp')), 0)
        self.assertEqual(len(self.files_in_folder(DATASTORE_PATH / 'incoming')), incoming)
        self.assertEqual(len(self.files_in_folder(DATASTORE_PATH / 'suspicious')), suspicious)

    def assert_num_events_written(self, number_of_events):
        file_path = self.files_in_folder(DATASTORE_PATH / 'incoming')[0]
        with file_path.open('rb') as file_handle:
            data = pickle.load(file_handle)
        written_event_list = data['event_list']
        self.assertEqual(len(written_event_list), number_of_events)
