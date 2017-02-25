import unittest
import requests
import functools
import hashlib
import pickle
import shutil
import sys
from io import StringIO

from webtest import TestApp


# configuration:
CONFIGFILE = 'test_data/config.ini'
WSGI_APP_PATH = '../wsgi'

STATION_ID = 99
PASSWORD = 'fake_station'

EVENTPY2 = 'test_data/incoming_http/py2event'
EVENTPY3 = 'test_data/incoming_http/py3event'
EVENTSUS = 'test_data/incoming_http/suspicious_event'


def import_wsgi_app():
    """import the WSGI application"""
    sys.path.append(WSGI_APP_PATH)
    import wsgi_app
    return functools.partial(wsgi_app.application, configfile=CONFIGFILE)


def get_wsgi_app(wsgi_app=import_wsgi_app()):
    """return the WSGI application"""
    return wsgi_app


class TestWsgiApp(unittest.TestCase):

    def setUp(self):
        self.station_id = STATION_ID
        self.password = PASSWORD
        self.app = TestApp(get_wsgi_app())

    def test_invalid_post_data(self):
        resp = self.app.post('/', {})
        self.assertEqual(resp.body, b'400') # invalid post data

    def test_unpickling_error(self):
        broken_pickle = b'aaaaa'
        resp = self.upload(broken_pickle)
        self.assertEqual(resp, b'208') # unpickle error

    def test_invalid_checksum(self):
        event_list = self.read_pickle(EVENTPY2)
        resp = self.upload(event_list, checksum=b'invalid')
        self.assertEqual(resp, b'201') # input error

    def test_invalid_station_id(self):
        event_list = self.read_pickle(EVENTPY2)
        self.station_id = 0 # invalid station
        resp = self.upload(event_list)
        self.assertEqual(resp, b'206') # invalid station id

    def test_invalid_password(self):
        event_list = self.read_pickle(EVENTPY2)
        self.password = 'wrong_password'
        resp = self.upload(event_list)
        self.assertEqual(resp, b'203') # wrong password

    def test_put_py2_event(self):
        event_list = self.read_pickle(EVENTPY2)
        # Make sure the eventlist is indeed pickled on Python 2
        with self.assertRaises(UnicodeDecodeError):
            pickle.loads(event_list)

        resp = self.upload(event_list)
        self.assertEqual(resp, b'100')

        # verify the event in /incoming

    def test_put_py3_event(self):
        event_list = self.read_pickle(EVENTPY3)
        # Make sure the python 3 pickle is indeed pickled on Python 3
        try:
            pickle.loads(event_list)
        except UnicodeDecodeError:
            self.fail('Data does not seem pickled on python 3')

        resp = self.upload(event_list)
        self.assertEqual(resp, b'100')

        # verify the event in /incoming

    def test_put_suspicious_event(self):
        event_list = self.read_pickle(EVENTSUS)
        resp = self.upload(event_list)
        self.assertEqual(resp, b'100')

        # verify the event in /suspicious

    def upload(self, pickled_data, checksum=None):
        """POST. Return response"""

        if checksum is None:
            checksum = hashlib.md5(pickled_data).hexdigest()

        data = {'station_id': self.station_id,
                'password': self.password,
                'data': pickled_data.decode('latin-1'),
                'checksum': checksum}

        response = self.app.post('/', data)
        return response.body

    def read_pickle(self, fn):
        with open(fn, 'rb') as f:
            pickle = f.read()
        return pickle


if __name__ == '__main__':
    unittest.main()
