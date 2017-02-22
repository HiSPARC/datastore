import unittest
import requests
import hashlib
import pickle
import shutil


uWSGI_URL = 'http://localhost:80'
EVENTPY2 = 'test_data/incoming_http/py2event'
EVENTPY3 = 'test_data/incoming_http/py3event'
EVENTSUS = 'test_data/incoming_http/suspicious_event'


class Uploader(object):

    def __init__(self, url, sn, password):
        self.url = url
        self.station_id = sn
        self.password = password

    def upload_data(self, pickled_data, checksum=None):
        """Upload event data to wsgi-app.

        :param pickled_data: pickled event data (bytestring).
        :param checksum: optional checksum to send.

        returns the rcode or raises UploadError.

        """
        if checksum is None:
            checksum = hashlib.md5(pickled_data).hexdigest()

        payload = {'station_id': self.station_id,
                   'password': self.password, 'data': pickled_data.decode('latin-1'),
                   'checksum': checksum}
        try:
            r = requests.post(self.url, data=payload, timeout=10)
            r.raise_for_status()
        except (ConnectionError) as exc:
            raise UploadError(str(exc))
        else:
            return r.text


class TestWsgiApp(unittest.TestCase):

    url = uWSGI_URL
    uploader = Uploader(url, 99, 'fake_station')
    pickled_eventlist_py2 = open(EVENTPY2, 'rb').read()
    pickled_eventlist_py3 = open(EVENTPY3, 'rb').read()
    suspicious_eventlist = open(EVENTSUS, 'rb').read()

    def setUp(self):
        # clean fake_datstore
        pass
 
    def test_invalid_post_data(self):
        r = requests.post(self.url, data={}, timeout=10)
        self.assertEqual(r.text, '400') # invalid post data

    def test_unpickling_error(self):
        broken_pickle = b'aaaaa'
        checksum = hashlib.md5(broken_pickle).hexdigest()
        r_text =  self.uploader.upload_data(broken_pickle, checksum=checksum)
        self.assertEqual(r_text, '208') # unpickle error

    def test_invalid_checksum(self):
        r_text = self.uploader.upload_data(self.pickled_eventlist_py2,
                                           checksum=b'invalid')
        self.assertEqual(r_text, '201') # input error

    def test_invalid_station_id(self):
        uploader = Uploader(self.url, 0, 'password')
        r_text = uploader.upload_data(self.pickled_eventlist_py2)
        self.assertEqual(r_text, '206') # invalid station_id

    def test_invalid_password(self):
        uploader = Uploader(self.url, 99, 'wrong_password')
        r_text = uploader.upload_data(self.pickled_eventlist_py2)
        self.assertEqual(r_text, '203') # wrong password

    def test_put_py2_event(self):
        # Make sure the python 2 pickle throws UnicodeDecodeError
        with self.assertRaises(UnicodeDecodeError):
            pickle.loads(self.pickled_eventlist_py2)

        r_text = self.uploader.upload_data(self.pickled_eventlist_py2)
        self.assertEqual(r_text, '100') # OK

        # verify the event in /incoming

    def test_put_py3_event(self):
        # Make sure the python 3 pickle is indeed pickled on Python 3
        try:
            pickle.loads(self.pickled_eventlist_py3)
        except UnicodeDecodeError:
            self.fail('Data does not seem pickled on python 3')

        r_text = self.uploader.upload_data(self.pickled_eventlist_py3)
        self.assertEqual(r_text, '100') # OK

        # verify the event in /incoming

    def test_put_suspicious_event(self):
        r_text = self.uploader.upload_data(self.suspicious_eventlist)
        self.assertEqual(r_text, '100') # OK

        # verify the event in /suspicious


if __name__ == '__main__':
    unittest.main()
