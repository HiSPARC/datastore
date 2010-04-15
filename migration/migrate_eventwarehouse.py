""" Migrate eventwarehouse data to the datastore

    This module will migrate all available data in the eventwarehouse to
    our new datastore using the regular datastore workflow.  That means
    that we won't circumvent the usual upload / writer cycle.  This module
    will download data from the eventwarehouse and write files to the
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
import base64
import csv

from settings import *

class Database:
    def __init__(self):
        self.open()

    def open(self):
        self.db = MySQLdb.connect(host=EWH_HOST, user=EWH_USER,
                                  passwd=EWH_PASSWD, db=EWH_DB,
                                  port=EWH_PORT)

    def close(self):
        self.db.close()

    def get_cursor(self):
        return self.db.cursor()


def migrate():
    """Migrate data from eventwarehouse to datastore"""

    status = read_migration_status()
    clusters = read_station_list()
    eventwarehouse = Database()

    logger.info("Starting migration of all data...")
    for station in get_stations(eventwarehouse):
        migrate_data(eventwarehouse, status, station, clusters)
    logger.info("Migrating all data finished succesfully.")

def read_migration_status():
    """Read migration status from file"""

    try:
        with open(EWH_STATUS, 'r') as file:
            status = pickle.load(file)
    except IOError:
        status = {}

    return status

def write_migration_status(status):
    """Write migration status to file"""

    with open(EWH_STATUS, 'w') as file:
        pickle.dump(status, file)

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

def get_stations(eventwarehouse):
    """Return all stations which have data in the eventwarehouse"""

    sql = "SELECT station_id FROM event GROUP BY station_id"
    results = execute_and_results(eventwarehouse, sql)
    station_list = [x[0] for x in results]

    return station_list

def migrate_data(eventwarehouse, status, station, clusters):
    """Migrate data for a station"""

    logger.info("Starting migration for station %d" % station)
    for start, end, batch in get_event_batches(eventwarehouse, status,
                                               station):
        logger.info("Migrating batch from %s to %s" % (start, end))
        store_events(batch, station, clusters)
        write_migration_status(status)
        logger.info("Done.")

def get_event_batches(eventwarehouse, status, station):
    """Generator function yielding batches of events for a station"""

    if not status.has_key(station):
        status[station] = '1970-1-1', None

    for date in get_station_date_list(eventwarehouse, status, station):
        if date == status[station][0]:
            offset = status[station][1] + BATCHSIZE
        else:
            offset = 0

        while True:
            events = get_events(eventwarehouse, station, date, offset,
                                BATCHSIZE)
            if not events:
                break
            else:
                get_event_data(eventwarehouse, events)
                get_calculated_data(eventwarehouse, events)
                status[station] = date, offset
                offset += BATCHSIZE

                events = events.values()
                dts = [x['header']['datetime'] for x in events]
                yield min(dts), max(dts), events

def get_station_date_list(eventwarehouse, status, station):
    """Get date list for a station"""

    start = status[station][0]
    sql = ("SELECT date FROM event WHERE station_id=%s AND "
           "eventtype_id=1 AND date >= %s AND date < '2009-12-1' GROUP "
           "BY date")
    results = execute_and_results(eventwarehouse, sql, (station, start))
    return [x[0] for x in results]

def get_events(eventwarehouse, station, date, offset, limit):
    """Get data from event table"""

    sql = ("SELECT event_id, date, time, nanoseconds FROM event WHERE "
           "station_id=%s AND eventtype_id=1 AND date=%s "
           "LIMIT %s OFFSET %s")
    results = execute_and_results(eventwarehouse, sql, (station, date,
                                                        limit, offset))

    events = {}
    for event_id, date, time, nanoseconds in results:
        dt = datetime.datetime.combine(date, datetime.time()) + time
        events[event_id] = {'header': {'datetime': dt,
                                       'nanoseconds': nanoseconds,
                                       'eventtype_uploadcode': 'CIC'},
                            'datalist': []}
    return events

def get_event_data(eventwarehouse, events):
    """Get data from eventdata table and add it to events dictionary"""

    event_ids = ','.join([str(x) for x in events])
    sql = ("SELECT event_id, uploadcode, valuefield, integervalue, "
           "doublevalue, textvalue, blobvalue FROM eventdata JOIN "
           "eventdatatype USING(eventdatatype_id) JOIN valuetype "
           "USING(valuetype_id) WHERE event_id IN (%s)" % event_ids)
    results = execute_and_results(eventwarehouse, sql)

    for (event_id, uploadcode, valuefield, integervalue, doublevalue,
        textvalue, blobvalue) in results:
        exec('value = %s' % valuefield)
        if uploadcode[:-1] == 'TR':
            value = base64.b64encode(value)
        events[event_id]['datalist'].append(
            {'data_uploadcode': uploadcode, 'data': value})

def get_calculated_data(eventwarehouse, events):
    """Get data from calculateddata table and add it to events dictionary"""

    event_ids = ','.join([str(x) for x in events])
    sql = ("SELECT event_id, uploadcode, valuefield, integervalue, "
           "doublevalue FROM calculateddata JOIN calculateddatatype "
           "USING(calculateddatatype_id) JOIN valuetype "
           "USING(valuetype_id) WHERE event_id IN (%s)" % event_ids)
    results = execute_and_results(eventwarehouse, sql)

    for event_id, uploadcode, valuefield, integervalue, doublevalue in \
        results:
        exec('value = %s' % valuefield)
        events[event_id]['datalist'].append(
            {'data_uploadcode': uploadcode, 'data': value})

def store_events(event_list, station, clusters):
    """Store an event batch in the datastore incoming directory"""

    if station in renumbered_stations:
        station = renumbered_stations[station]

    # Do not migrate KASCADE data
    if station == 99999:
        return

    cluster = clusters[station]

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
