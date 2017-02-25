import unittest
import functools
import hashlib
import glob
import os
import pickle
import sys

from webtest import TestApp


# configuration:
CONFIGFILE = 'test_data/config.ini'
WSGI_APP_PATH = '../wsgi'
DATASTORE_PATH = 'fake_datastore'

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

    def tearDown(self):
        self.clean_datastore()

    def test_invalid_post_data(self):
        resp = self.app.post('/', {})
        self.assertEqual(resp.body, b'400')  # invalid post data
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

    def test_put_suspicious_event(self):
        event_list = self.read_pickle(EVENTSUS)
        resp = self.upload(event_list)
        self.assertEqual(resp, b'100')
        self.assert_num_files_in_datastore(suspicious=1)

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

    def files_in_folder(self, folder):
        return glob.glob(folder+'/*')

    def clean_datastore(self):
        for folder in ['/incoming', '/tmp', '/suspicious']:
            for fn in self.files_in_folder(DATASTORE_PATH+folder):
                os.remove(fn)

    def assert_num_files_in_datastore(self, incoming=None, suspicious=None):
        self.assertEqual(len(self.files_in_folder(DATASTORE_PATH+'/tmp')), 0)
        if incoming is not None:
            self.assertEqual(
                len(self.files_in_folder(DATASTORE_PATH+'/incoming')),
                incoming)
        if suspicious is not None:
            self.assertEqual(
                len(self.files_in_folder(DATASTORE_PATH+'/suspicious')),
                suspicious)


if __name__ == '__main__':
    unittest.main()
