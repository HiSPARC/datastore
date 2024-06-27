"""datastore writer application

This module empties the station data `incoming` queue and writes the
data into HDF5 files using PyTables.

"""

import configparser
import logging
import logging.handlers
import pickle
import time

from pathlib import Path

from writer.store_events import store_event_list

LEVELS = {
    'debug': logging.DEBUG,
    'info': logging.INFO,
    'warning': logging.WARNING,
    'error': logging.ERROR,
    'critical': logging.CRITICAL,
}

logger = logging.getLogger('writer')
formatter = logging.Formatter('%(asctime)s %(name)s[%(process)d].%(funcName)s.%(levelname)s: %(message)s')


def writer(configfile):
    """hisparc datastore writer application

    This script polls ``/datatore/frome/incoming`` for incoming data written
    by the WSGI app. It then store the data into the raw datastore.

    Configuration is read from the datastore configuation file (usually
    `config.ini`):

    .. include:: ../examples/config.ini
       :literal:

    """
    # set up config
    global config
    config = configparser.ConfigParser()
    config.read(configfile)

    # set up logger
    file = config.get('General', 'log') + '-writer'
    handler = logging.handlers.TimedRotatingFileHandler(file, when='midnight', backupCount=14)
    handler.setFormatter(formatter)
    logger.addHandler(handler)
    level = LEVELS.get(config.get('General', 'loglevel'), logging.NOTSET)
    logger.setLevel(level=level)

    data_dir = Path(config.get('General', 'data_dir'))
    queue = data_dir /  'incoming'
    partial_queue = data_dir / 'partial'

    sleep_duration = config.getint('Writer', 'sleep')

    # writer process
    try:
        while True:
            entries = queue.iterdir()

            if not entries:
                time.sleep(sleep_duration)

            for entry in entries:
                partial_path = partial_queue / entry.name
                entry.rename(partial_path)

                process_data(partial_path, data_dir)
                partial_path.unlink()

    except Exception:
        logger.exception('Exception occured, quitting.')


def process_data(file, data_dir):
    """Read data from a pickled object and store store in raw datastore"""
    with file.open('rb') as handle:
        try:
            data = pickle.load(handle)
        except UnicodeDecodeError:
            logger.debug('Data seems to be pickled using python 2. Decoding.')
            data = decode_object(pickle.load(handle, encoding='bytes'))

    logger.debug(f"Processing data for station {data['station_id']}")
    store_event_list(data_dir, data['station_id'], data['cluster'], data['event_list'])


def decode_object(o):
    """recursively decode all bytestrings in object"""

    if isinstance(o, bytes):
        return o.decode()
    elif isinstance(o, dict):
        return {decode_object(k): decode_object(v) for k, v in o.items()}
    elif isinstance(o, list):
        return [decode_object(obj) for obj in o]
    else:
        return o
