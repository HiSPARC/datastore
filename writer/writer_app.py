""" datastore writer application

    This module empties the station data `incoming` queue and writes the
    data into HDF5 files using PyTables.

"""
import logging
import logging.handlers
import configparser
import os
import time
import pickle as pickle
import shutil

from writer.store_events import store_event_list

LEVELS = {'debug': logging.DEBUG,
          'info': logging.INFO,
          'warning': logging.WARNING,
          'error': logging.ERROR,
          'critical': logging.CRITICAL}

logger = logging.getLogger('writer')
formatter = logging.Formatter('%(asctime)s %(name)s[%(process)d]'
                              '.%(funcName)s.%(levelname)s: %(message)s')


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
    handler = logging.handlers.TimedRotatingFileHandler(file,
                                                        when='midnight',
                                                        backupCount=14)
    handler.setFormatter(formatter)
    logger.addHandler(handler)
    level = LEVELS.get(config.get('General', 'loglevel'), logging.NOTSET)
    logger.setLevel(level=level)

    queue = os.path.join(config.get('General', 'data_dir'), 'incoming')
    partial_queue = os.path.join(config.get('General', 'data_dir'),
                                 'partial')

    # writer process
    try:
        while True:
            entries = os.listdir(queue)

            if not entries:
                time.sleep(config.getint('Writer', 'sleep'))

            for entry in entries:
                path = os.path.join(queue, entry)
                shutil.move(path, partial_queue)

                path = os.path.join(partial_queue, entry)
                process_data(path)
                os.remove(path)
    except Exception:
        logger.exception('Exception occured, quitting.')


def process_data(file):
    """Read data from a pickled object and store store in raw datastore"""
    with open(file, 'rb') as handle:
        try:
            data = pickle.load(handle)
        except UnicodeDecodeError:
            logger.debug('Data seems to be pickled using python 2. Decoding.')
            data = decode_object(pickle.load(handle, encoding='bytes'))

    logger.debug('Processing data for station %d' % data['station_id'])
    store_event_list(config.get('General', 'data_dir'),
                     data['station_id'], data['cluster'], data['event_list'])


def decode_object(o):
    """recursively decode all bytestrings in object"""

    if type(o) is bytes:
        return o.decode()
    elif type(o) is dict:
        return {decode_object(k): decode_object(v) for k, v in o.items()}
    elif type(o) is list:
        return [decode_object(obj) for obj in o]
    else:
        return o
