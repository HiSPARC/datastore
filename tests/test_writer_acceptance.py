"""Acceptance tests for the writer

Check with data pickled by Python 2 and 3.

"""

import base64
import configparser
import shutil
import unittest

from pathlib import Path
from unittest import mock

import tables

from numpy import array
from numpy.testing import assert_array_equal

from writer import writer_app

self_path = Path(__file__).parent
test_data_path = self_path / 'test_data'

# Configuration
DATASTORE_PATH = self_path / 'fake_datastore'
CONFIGFILE = test_data_path / 'config.ini'
STATION_ID = 99
CLUSTER = 'amsterdam'

UPLOAD_CODES = ['CIC', 'SIN', 'WTR', 'CFG']
PICKLE_DATA_PATH = test_data_path / 'incoming_writer'


def configure_writer_app():
    """configure the writer"""
    writer_app.config = configparser.ConfigParser()
    writer_app.config.read(CONFIGFILE)
    return writer_app


def get_writer_app(writer_app=None):
    """return the WSGI application"""
    if not hasattr(writer_app, 'config'):
        writer_app = configure_writer_app()
    return writer_app


@mock.patch('writer.store_events.MINIMUM_YEAR', 2016)
class TestWriterAcceptancePy2Pickles(unittest.TestCase):
    """Acceptance tests for python 2 pickles"""

    pickle_version = 'py2'

    def setUp(self):
        self.writer_app = get_writer_app()
        self.station_id = STATION_ID
        self.cluster = CLUSTER
        self.filepath = '2017/2/2017_2_26.h5'
        self.pickle_filename = {
            upload_code: PICKLE_DATA_PATH / f'writer_{self.pickle_version}_{upload_code}'
            for upload_code in UPLOAD_CODES
        }

    def tearDown(self):
        shutil.rmtree(DATASTORE_PATH / '2017')

    def test_event_acceptance(self):
        self.writer_app.process_data(self.pickle_filename['CIC'], DATASTORE_PATH)

        data = self.read_table('events')
        self.assertEqual(data['timestamp'], 1488093964)
        self.assertEqual(data['nanoseconds'], 130245552)
        assert_array_equal(data['pulseheights'], array([[625, 972, 923, 724]]))

        blobs = self.read_table('blobs')
        self.assertEqual(len(blobs), 4)
        # traces are sent base64 encoded and decoded by the writer
        tr1 = blobs[0]
        tr1_b64 = (
            b'eJxtkFkOAyEMQy/kD7KH+1+sBmZppUoZCI+MQ6wT+kT/5vfRxopD3rze'
            b'ygMvfojBFTkhllA3WDVCiIYjfSKDO+9yJKIKEbx3R+iAt8OtYM3PliQ1'
            b'i+qUVDFIJyQbQh1hP6HuTJBWgDwmpeAFD/hJEqwNRbCbsRnfsoj3LlA4'
            b'j5yAs/oO3THWHI8BJnsy+TLmEL4y7zXXL+Rr1WXSH2/GNu+KD4ouSr4='
        )
        self.assertEqual(tr1, base64.decodebytes(tr1_b64))

    def test_singles_acceptance(self):
        self.writer_app.process_data(self.pickle_filename['SIN'], DATASTORE_PATH)

        data = self.read_table('singles')
        self.assertEqual(data['timestamp'], 1488094031)
        self.assertEqual(data['mas_ch1_low'], 345)
        self.assertEqual(data['mas_ch1_high'], 98)
        self.assertEqual(data['slv_ch1_low'], 329)
        self.assertEqual(data['slv_ch1_high'], 95)

        blobs = self.read_table('blobs')
        self.assertEqual(len(blobs), 0)

    def test_weather_acceptance(self):
        self.writer_app.process_data(self.pickle_filename['WTR'], DATASTORE_PATH)

        data = self.read_table('weather')
        self.assertEqual(data['timestamp'], 1488094084)
        self.assertEqual(data['uv'], -999)
        self.assertAlmostEqual(data['barometer'], 1004.365)
        self.assertEqual(data['humidity_inside'], 25)

        blobs = self.read_table('blobs')
        self.assertEqual(len(blobs), 0)

    def test_config_acceptance(self):
        self.writer_app.process_data(self.pickle_filename['CFG'], DATASTORE_PATH)
        data = self.read_table('config')
        self.assertEqual(data['timestamp'], 1488125225)
        self.assertEqual(data['mas_ch1_thres_high'], 320)
        self.assertEqual(data['mas_ch1_thres_low'], 250)
        self.assertEqual(data['reduce_data'], False)
        self.assertAlmostEqual(data['mas_ch1_voltage'], 300)
        self.assertAlmostEqual(data['slv_ch1_current'], 0.0)

        blobs = self.read_table('blobs')
        self.assertEqual(len(blobs), 2)
        self.assertEqual(blobs[0], b'')
        self.assertEqual(blobs[1], b'Hardware: 0 FPGA: 0')

    def read_table(self, table):
        path = DATASTORE_PATH / self.filepath
        table_path = f'/hisparc/cluster_{self.cluster}/station_{self.station_id}/{table}'
        with tables.open_file(path, 'r') as datafile:
            t = datafile.get_node(table_path)
            data = t.read()

        return data


class TestWriterAcceptancePy3Pickles(TestWriterAcceptancePy2Pickles):
    """Acceptance tests for python 3 pickles"""

    pickle_version = 'py3'


if __name__ == '__main__':
    unittest.main()
