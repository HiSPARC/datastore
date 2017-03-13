"""
compare datastore files

Compare each 'expected_yyyy_mm_dd.h5' with 'yyyy_mm_dd.h5'

usage:
python compare.py

"""

import glob
import unittest
import os

import tables
from numpy.testing import assert_array_equal


class TestDataStoreAcceptance(unittest.TestCase):

    def _validate_results(self, expected_path, actual_path):
        """Validate results by comparing in and output HDF5 files
        :param test: instance of the TestCase.
        :param expected_path: path to the reference data.
        :param actual_path: path to the output from the test.

        From sapphire.tests.validate_results
        """
        with tables.open_file(expected_path, 'r') as expected_file, \
                tables.open_file(actual_path, 'r') as actual_file:
            for expected_node in expected_file.walk_nodes('/', 'Leaf'):
                try:
                    actual_node = actual_file.get_node(expected_node._v_pathname)
                except tables.NoSuchNodeError:
                    self.fail("Node '%s' does not exist in datafile" %
                              expected_node._v_pathname)
                self.assertEqual(expected_node.shape, actual_node.shape,
                                 "VLArrays '%s' do not have the same shape." %
                                 expected_node._v_pathname)
                if type(expected_node) is tables.table.Table:
                    self._compare_timestamps(expected_node, actual_node)
                elif type(expected_node) is tables.vlarray.VLArray:
                    self._compare_blobs(expected_node, actual_node)


    def _compare_blobs(self, expected_node, actual_node):
        """Verify that two blobs are identical"""

        expected = expected_node.read()
        expected.sort()
        actual = actual_node.read()
        actual.sort()
        assert_array_equal(expected, actual)


    def _compare_timestamps(self, expected_node, actual_node):
        """Verify that two tables have identical timestamps"""

        expected = expected_node.col('timestamp')
        expected.sort()
        actual = actual_node.col('timestamp')
        actual.sort()
        assert_array_equal(expected, actual)


def create_test(expected_path, actual_path):
    """Return test case for specific combination of paths"""
    def test_datastore_files(self):
        self.assertTrue(os.path.exists(expected_path))
        self._validate_results(expected_path, actual_path)
    return test_datastore_files


if __name__ == '__main__':
    # add a test case for each 'expected_' file
    files = glob.glob('expected_*.h5')
    for expected_path in files:
        actual_path = expected_path[9:]
        test = create_test(expected_path, actual_path)
        setattr(TestDataStoreAcceptance, 'test_%s' % actual_path, test)

    unittest.main()
