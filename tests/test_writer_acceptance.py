"""
Acceptance tests for the writer

python 3
"""
import unittest
import base64
import configparser
import shutil
import sys
import tables

from numpy import array
from numpy.testing import assert_array_equal

# configuration:
CONFIGFILE = 'test_data/config.ini'
WRITER_PATH = '../writer'
DATASTORE_PATH = 'fake_datastore'

STATION_ID = 99
CLUSTER = 'amsterdam'

CIC_PY2 = 'test_data/incoming_writer/writer_py2_CIC'
SIN_PY2 = 'test_data/incoming_writer/writer_py2_SIN'
WTR_PY2 = 'test_data/incoming_writer/writer_py2_WTR'
CFG_PY2 = 'test_data/incoming_writer/writer_py2_CFG'


def import_writer():
    """import the writer"""
    sys.path.append(WRITER_PATH)
    import writer
    writer.config = configparser.ConfigParser()
    writer.config.read(CONFIGFILE)
    return writer


def get_writer(writer=import_writer()):
    """return the WSGI application"""
    return writer


class TestWriterAcceptance(unittest.TestCase):

    def setUp(self):
        self.writer = get_writer()
        self.station_id = STATION_ID
        self.cluster = CLUSTER
        self.filename = '2017_2_26.h5'

    def tearDown(self):
        self.clean_datastore()

    def test_event_acceptance(self):
        self.writer.process_data(CIC_PY2)

        data = self.read_table('events')
        self.assertEqual(data['timestamp'], 1488093964)
        self.assertEqual(data['nanoseconds'], 130245552)
        assert_array_equal(data['pulseheights'], array([[625, 972, 923, 724]]))

        blobs = self.read_table('blobs')
        self.assertEqual(len(blobs), 4)
        # traces are sent base64 encoded and decoded by the writer
        tr1 = blobs[0]
        tr1_b64 = (b'eJxtkFkOAyEMQy/kD7KH+1+sBmZppUoZCI+MQ6wT+kT/5vfRxopD3rze'
                   b'ygMvfojBFTkhllA3WDVCiIYjfSKDO+9yJKIKEbx3R+iAt8OtYM3PliQ1'
                   b'i+qUVDFIJyQbQh1hP6HuTJBWgDwmpeAFD/hJEqwNRbCbsRnfsoj3LlA4'
                   b'j5yAs/oO3THWHI8BJnsy+TLmEL4y7zXXL+Rr1WXSH2/GNu+KD4ouSr4=')
        self.assertEqual(tr1, base64.decodebytes(tr1_b64))

    def test_singles_acceptance(self):
        self.writer.process_data(SIN_PY2)

        data = self.read_table('singles')
        self.assertEqual(data['timestamp'], 1488094031)
        self.assertEqual(data['mas_ch1_low'], 345)
        self.assertEqual(data['mas_ch1_high'], 98)
        self.assertEqual(data['slv_ch1_low'], 329)
        self.assertEqual(data['slv_ch1_high'], 95)

        blobs = self.read_table('blobs')
        self.assertEqual(len(blobs), 0)

    def test_weather_acceptance(self):
        self.writer.process_data(WTR_PY2)

        data = self.read_table('weather')
        self.assertEqual(data['timestamp'], 1488094084)
        self.assertEqual(data['uv'], -999)
        self.assertAlmostEqual(data['barometer'], 1004.365)
        self.assertEqual(data['humidity_inside'], 25)

        blobs = self.read_table('blobs')
        self.assertEqual(len(blobs), 0)

    def test_config_acceptance(self):
        self.writer.process_data(CFG_PY2)
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
        year, month, _ = self.filename.split('_')
        path = DATASTORE_PATH+'/'+year+'/'+month+'/'+self.filename
        table_path = '/hisparc/cluster_%s/station_%s/%s' % (self.cluster,
                                                            self.station_id,
                                                            table)
        with tables.open_file(path, 'r') as datafile:
            t = datafile.get_node(table_path)
            data = t.read()

        return data

    def clean_datastore(self):
        shutil.rmtree(DATASTORE_PATH+'/2017')


if __name__ == '__main__':
    unittest.main()
