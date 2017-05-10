"""
Acceptance tests for the writer

python 3
"""
import unittest
import base64
import configparser
import os
import shutil
import sys
import tables

from numpy import array
from numpy.testing import assert_array_equal


self_path = os.path.dirname(__file__)
test_data_path = os.path.join(self_path, 'test_data/')

# configuration:
WRITER_PATH = os.path.join(self_path, '../')
DATASTORE_PATH = os.path.join(self_path, 'fake_datastore')
CONFIGFILE = os.path.join(test_data_path, 'config.ini')

CONFIG = """
[General]
log=hisparc.log
loglevel=debug
station_list={datastore}/station_list.csv
data_dir={datastore}
""".format(datastore=DATASTORE_PATH)

with open(CONFIGFILE, 'w') as f:
    f.write(CONFIG)

STATION_ID = 99
CLUSTER = 'amsterdam'

UPLOAD_CODES = ['CIC', 'SIN', 'WTR', 'CFG']
pickle_data_path = os.path.join(test_data_path, 'incoming_writer/')


def import_writer():
    """import the writer"""
    sys.path.append(WRITER_PATH)
    from writer import writer
    writer.config = configparser.ConfigParser()
    writer.config.read(CONFIGFILE)
    return writer


def get_writer(writer=import_writer()):
    """return the WSGI application"""
    return writer


class TestWriterAcceptancePy2Pickles(unittest.TestCase):
    """Acceptance tests for python 2 pickles"""
    pickle_version = 'py2'

    def setUp(self):
        self.writer = get_writer()
        self.station_id = STATION_ID
        self.cluster = CLUSTER
        self.filename = '2017_2_26.h5'
        self.pickle_filename = {}
        for upload_code in UPLOAD_CODES:
            self.pickle_filename[upload_code] = os.path.join(
                pickle_data_path, 'writer_%s_%s' % (self.pickle_version,
                                                    upload_code))

    def tearDown(self):
        self.clean_datastore()

    def test_event_acceptance(self):
        self.writer.process_data(self.pickle_filename['CIC'])

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
        self.writer.process_data(self.pickle_filename['SIN'])

        data = self.read_table('singles')
        self.assertEqual(data['timestamp'], 1488094031)
        self.assertEqual(data['mas_ch1_low'], 345)
        self.assertEqual(data['mas_ch1_high'], 98)
        self.assertEqual(data['slv_ch1_low'], 329)
        self.assertEqual(data['slv_ch1_high'], 95)

        blobs = self.read_table('blobs')
        self.assertEqual(len(blobs), 0)

    def test_weather_acceptance(self):
        self.writer.process_data(self.pickle_filename['WTR'])

        data = self.read_table('weather')
        self.assertEqual(data['timestamp'], 1488094084)
        self.assertEqual(data['uv'], -999)
        self.assertAlmostEqual(data['barometer'], 1004.365)
        self.assertEqual(data['humidity_inside'], 25)

        blobs = self.read_table('blobs')
        self.assertEqual(len(blobs), 0)

    def test_config_acceptance(self):
        self.writer.process_data(self.pickle_filename['CFG'])
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


class TestWriterAcceptancePy3Pickles(TestWriterAcceptancePy2Pickles):
    """Acceptance tests for python 3 pickles"""
    pickle_version = 'py3'


if __name__ == '__main__':
    unittest.main()
