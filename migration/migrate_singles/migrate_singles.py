"""

Migrate singles tables to new HisparcSingle format.

HisparcSingle columns where `tables.UInt16Col` before
HiSPARC/datastore@dec64079. Convert old tables to the new format.
For a missing slave (two detector stations) the slave columns where set
to all zero, instead of all `-1`. Set those columns to `-1`

logging to logfile `migration.log`
prints progressbars for searching and processing tables.

"""
from __future__ import print_function

import glob
import logging
import re

import numpy as np
import tables
from sapphire.utils import pbar
from sapphire import HiSPARCNetwork


DATASTORE_PATH = '/data/hisparc/tom/Datastore/frome/'
# DATASTORE_PATH = '/databases/frome/'


class MigrateSingles(object):
    """Migrate singles to new table format
       If the station has no slave *and* slave columns are all zero,
       replace slave columns with `-1` to correctly represent missing slave.
    """

    class HisparcSingle(tables.IsDescription):
        event_id = tables.UInt32Col(pos=0)
        timestamp = tables.Time32Col(pos=1)
        mas_ch1_low = tables.Int32Col(dflt=-1, pos=2)
        mas_ch1_high = tables.Int32Col(dflt=-1, pos=3)
        mas_ch2_low = tables.Int32Col(dflt=-1, pos=4)
        mas_ch2_high = tables.Int32Col(dflt=-1, pos=5)
        slv_ch1_low = tables.Int32Col(dflt=-1, pos=6)
        slv_ch1_high = tables.Int32Col(dflt=-1, pos=7)
        slv_ch2_low = tables.Int32Col(dflt=-1, pos=8)
        slv_ch2_high = tables.Int32Col(dflt=-1, pos=9)

    def __init__(self, data):
        self.data = data
        self.singles_dtype = \
            tables.description.dtype_from_descr(self.HisparcSingle)
        self.network = HiSPARCNetwork(force_stale=True)

    def migrate_table(self, table_path):
        """Migrate datatable to new format. Fix slave columns."""

        logging.info('Migrating table: %s' % table_path)
        group, table_name, sn = self._parse_path(table_path)

        if table_name != 'singles':
            logging.error('Table %s not `singles` skipping!' % table_path)
            return None

        tmp_table_name = '_t_%s' % table_name

        try:
            tmptable = self.data.create_table(group, tmp_table_name,
                                              description=self.HisparcSingle)
        except tables.NodeError:
            logging.error('%s/_t_%s exists. Removing.' % (group, table_name))
            self.data.remove_node(group, '_t_%s' % table_name)
            tmptable = self.data.create_table(group, tmp_table_name,
                                              description=self.HisparcSingle)

        table = self.data.get_node(table_path)
        data = table.read()
        data = data.astype(self.singles_dtype)
        if not self._has_slave(sn):
            data = self._mark_slave_columns_as_missing(data)

        tmptable.append(data)
        tmptable.flush()
        self.data.rename_node(table, 'singles_old')
        self.data.rename_node(tmptable, 'singles')

    def _parse_path(self, path):
        """ '/cluster/s501/singles' ---> '/cluster/s501' 'singles', 501 """

        group, table_name = tables.path.split_path(path)
        re_number = re.compile('[0-9]+$')
        numbers = [int(re_number.search(group).group())]
        sn = numbers[-1]
        return group, table_name, sn

    def _has_slave(self, sn):
        """Return True if station (sn) has slave (4 detectors)"""
        try:
            n_detectors = len(self.network.get_station(sn).detectors)
        except AttributeError:
            logging.error('No information in HiSPARCNetwork() for sn %d' % sn)
            n_detectors = 4
        return n_detectors == 4

    def _mark_slave_columns_as_missing(self, table):
        """Replace slave columns with `-1`"""

        cols = ['slv_ch1_low', 'slv_ch2_low', 'slv_ch1_high', 'slv_ch2_high']
        for col in cols:
            if not np.all(table[col] == 0):
                logging.error("Slave columns are not all zero. "
                              "Leaving data untouched!")
                return table

        n = len(table)
        for col in cols:
            table[col] = n * [-1]

        logging.debug("Set all slave columns to `-1`.")
        return table


def get_queue(datastore_path):
    queue = {}
    logging.info('Searching for unmigrated singles tables')

    print('Looking for singles tables in datastore.')

    # Singles tables were added in Feb, 2016.
    for fn in pbar(glob.glob(datastore_path + '/201[6,7]/*/*h5')):

        singles_tables = []
        with tables.open_file(fn, 'r') as data:
            for node in data.walk_nodes('/', 'Table'):
                table_path = node._v_pathname
                if '/singles' in table_path:
                    type_ = type(node.description.mas_ch1_low)
                    if type_ == tables.UInt16Col:
                        logging.debug('Found: %s' % table_path)
                        singles_tables.append(table_path)
                    elif type_ == tables.Int32Col:
                        logging.debug('Skipping migrated: %s' % table_path)
                        continue
                    else:
                        logging.error('%s in unknown format!' % table_path)

        if singles_tables:
            queue[fn] = singles_tables
            logging.info('Found %d tables in %s' % (len(singles_tables), fn))

    n = sum(len(v) for v in queue.itervalues())
    logging.info('Found %d unmigrated tables '
                 'in %d datastore files.' % (n, len(queue)))
    return queue


def migrate():
    """
    Find unmigrated tables in datastore
    migrate tables
    check datastore again for unmigrated tables
    """

    logging.info('******************')
    logging.info('Starting migration')
    logging.info('******************')

    queue = get_queue(DATASTORE_PATH)
    print('migrating:')
    for path in pbar(queue.keys()):
        logging.info('Migrating: %s' % path)
        with tables.open_file(path, 'a') as data:
            migration = MigrateSingles(data)
            for table in queue[path]:
                logging.debug('Processing table: %s' % table)
                migration.migrate_table(table)

    queue = get_queue(DATASTORE_PATH)
    if queue:
        logging.error('Found unprocessed tables after migration')
        for path in queue.keys():
            logging.error('Unprocessed tables in: %s' % path)
            for table in queue[path]:
                logging.error('%s' % table)
    else:
        logging.info('********************')
        logging.info('Migration succesful!')
        logging.info('********************')


if __name__ == '__main__':
    fmt = "%(asctime)s - %(levelname)s - %(message)s"
    logging.basicConfig(filename='migration.log', level=logging.INFO,
                        format=fmt)

    logging.info('Datastore path: %s', DATASTORE_PATH)
    migrate()
    logging.info('Done.')
