""" HDF5 writer application

    This module empties the station data `incoming' queue and writes the
    data into HDF5 files using PyTables.

"""
import logging
import logging.handlers
import ConfigParser
import os
import time
import cPickle as pickle
import shutil

from store_events import store_event_list

LEVELS = {'debug': logging.DEBUG,
          'info': logging.INFO,
          'warning': logging.WARNING,
          'error': logging.ERROR,
          'critical': logging.CRITICAL}

logger = logging.getLogger('writer')
formatter = logging.Formatter('%(asctime)s %(name)s[%(process)d]'
                              '.%(funcName)s.%(levelname)s: %(message)s')


def writer(configfile):
    # set up config
    global config
    config = ConfigParser.ConfigParser()
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
    except:
        logger.exception('Exception occured, quitting.')


def process_data(file):
    with open(file) as handle:
        data = pickle.load(handle)

    logger.debug('Processing data for station %d' % data['station_id'])
    store_event_list(config.get('General', 'data_dir'),
                     data['station_id'], data['cluster'], data['event_list'])
