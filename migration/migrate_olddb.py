""" Migrate old database data to the datastore

    This module will migrate all available data in the original database
    to our new datastore using the regular datastore workflow.  That means
    that we won't circumvent the usual upload / writer cycle.  This module
    will download data from the old database and write files to the
    'incoming' directory, in effect becoming an uploader by itself.  The
    writer will then pick up the data files and store them in the
    datastore.

"""
import logging
import MySQLdb
import datetime
import tempfile
import os
import shutil
import cPickle as pickle
import zlib
import csv
import re

from settings import *

class Database:
    def __init__(self):
        self.open()

    def open(self):
        self.db = MySQLdb.connect(host=OLDDB_HOST, user=OLDDB_USER,
                                  db=OLDDB_DB, port=OLDDB_PORT)

    def close(self):
        self.db.close()

    def get_cursor(self):
        return self.db.cursor()


def migrate():
    """Migrate data from original database to datastore"""

    status = read_migration_status()
    cluster = read_station_list()
    olddb = Database()

    logger.info("Starting migration of all data...")
    for table in get_data_tables(olddb):
        station = int(re.search('events([0-9]+)', table).group(1))

        # station-specific transformations
        if station in renumbered_stations:
            station = renumbered_stations[station]

        migrate_data(olddb, status, table, station, cluster[station])
    logger.info("Migrating all data finished succesfully.")

def read_migration_status():
    """Read migration status from file"""

    try:
        with open(OLDDB_STATUS, 'r') as file:
            status = pickle.load(file)
    except IOError:
        status = {}

    return status

def write_migration_status(status):
    """Write migration status to file"""

    with open(OLDDB_STATUS, 'w') as file:
        pickle.dump(status, file)

def get_data_tables(database):
    """Get all tables containing event data"""

    sql = "SHOW TABLES LIKE 'events%_%'"
    results = execute_and_results(database, sql)

    return [x[0] for x in results]

def read_station_list():
    """Read station, cluster combinations from file"""

    station_list = {}
    with open(STATION_LIST, 'r') as file:
        reader = csv.reader(file)
        for station in reader:
            if station:
                num, cluster, password = station
                num = int(num)
                station_list[num] = cluster
    return station_list

def migrate_data(database, status, table, station, cluster):
    """Migrate one data table"""

    if status.has_key(table):
        return
    else:
        logger.info("Migrating table %s" % table)
        status[table] = True
        events = get_events(database, table)
        events = process_events(events)
        store_events(events, station, cluster)
        write_migration_status(status)
        logger.info("Done.")

def get_events(database, table):
    """Get data from event table"""

    sql = ("SELECT trace1, trace2, rawPulseHeight1, rawPulseHeight2, "
           "rawIntegral1, rawIntegral2, rawBaseline1, rawBaseline2, "
           "rawNumPeaks1, rawNumPeaks2, trigDateTime, trigNanoSec FROM %s"
           % table)
    results = execute_and_results(database, sql)

    return results

def process_events(raw_events):
    """Build an event structure from supplied events"""

    events = []
    for event in raw_events:
        (tr1, tr2, ph1, ph2, in1, in2, bl1, bl2, np1, np2, trigdt,
         trigns) = event

        datalist = {}
        add_data(datalist, 'TR1', tr1)
        add_data(datalist, 'TR2', tr2)
        add_data(datalist, 'PH1', ph1)
        add_data(datalist, 'PH2', ph2)
        add_data(datalist, 'IN1', in1)
        add_data(datalist, 'IN2', in2)
        add_data(datalist, 'BL1', bl1)
        add_data(datalist, 'BL2', bl2)
        add_data(datalist, 'NP1', np1)
        add_data(datalist, 'NP2', np2)

        datalist = [{'data_uploadcode': x[0], 'data': x[1]} for x in
                    datalist.items()]

        events.append({'header': {'datetime': trigdt,
                                  'nanoseconds': trigns,
                       'eventtype_uploadcode': 'CIC'},
                       'datalist': datalist})

    return events

def add_data(datalist, key, value):
    """Add a key to the datalist if the value is meaningful"""

    if value:
        if key[:-1] == 'TR':
            value = zlib.compress(value)
        datalist[key] = value

def store_events(event_list, station, cluster):
    """Store an event batch in the datastore incoming directory"""

    dir = os.path.join(DATASTORE_PATH, 'incoming')
    tmp_dir = os.path.join(DATASTORE_PATH, 'tmp')

    file = tempfile.NamedTemporaryFile(dir=tmp_dir, delete=False)
    data = {'station_id': station, 'cluster': cluster,
            'event_list': event_list}
    pickle.dump(data, file)
    file.close()

    shutil.move(file.name, dir)

def execute_and_results(eventwarehouse, sql, *args):
    """Execute query and return results"""

    cursor = eventwarehouse.get_cursor()
    cursor.execute(sql, *args)

    results = cursor.fetchall()
    cursor.close()
    return results


if __name__ == '__main__':
    global logger
    logging.basicConfig(level=logging.DEBUG)
    logger = logging.getLogger('migrate')

    migrate()
