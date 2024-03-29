import configparser
import csv
import datetime
import hashlib
import logging
import logging.handlers
import os
import pickle as pickle
import shutil
import tempfile
import urllib.parse

from . import rcodes

LEVELS = {'debug': logging.DEBUG,
          'info': logging.INFO,
          'warning': logging.WARNING,
          'error': logging.ERROR,
          'critical': logging.CRITICAL}

logger = logging.getLogger('wsgi_app')
formatter = logging.Formatter('%(asctime)s %(name)s[%(process)d]'
                              '.%(funcName)s.%(levelname)s: %(message)s')


def application(environ, start_response, configfile):
    """ The hisparc upload application

    This handler is called by uWSGI whenever someone requests our URL.

    First, we generate a dictionary of POSTed variables and try to read out the
    station_id, password, checksum and data. When we do a readline(), we
    already read out the entire datastream. I don't know if we can first check
    on station_id/password combinations before reading out the datastream
    without setting up a bidirectional communication channel.

    When the checksum matches, we unpickle the event_list and pass everything
    on to store_event_list.

    """
    do_init(configfile)

    # start http response
    status = '200 OK'
    response_headers = [('Content-type', 'text/plain')]
    start_response(status, response_headers)

    # read data from the POST variables
    input = environ['wsgi.input'].readline().decode()
    vars = urllib.parse.parse_qs(input)

    # process POST data
    try:
        data = vars['data'][0]
        checksum = vars['checksum'][0]
        station_id = int(vars['station_id'][0])
        password = vars['password'][0]
    except (KeyError, EOFError):
        logger.debug("POST (vars) error")
        return [rcodes.RC_ISE_INV_POSTDATA]

    try:
        cluster, station_password = station_list[station_id]
    except KeyError:
        logger.debug("Station %d is unknown" % station_id)
        return [rcodes.RC_PE_INV_STATIONID]

    if station_password != password:
        logger.debug("Station %d: password mismatch: %s" % (station_id,
                                                            password))
        return [rcodes.RC_PE_INV_AUTHCODE]
    else:
        our_checksum = hashlib.md5(data.encode('iso-8859-1')).hexdigest()
        if our_checksum != checksum:
            logger.debug("Station %d: checksum mismatch" % station_id)
            return [rcodes.RC_PE_INV_INPUT]
        else:
            try:
                try:
                    event_list = pickle.loads(data.encode('iso-8859-1'))
                except UnicodeDecodeError:
                    # string was probably pickled on python 2.
                    # decode as bytes and decode all bytestrings to string.
                    logger.debug('UnicodeDecodeError on python 2 pickle.'
                                 ' Decoding bytestrings.')
                    event_list = decode_object(
                        pickle.loads(data.encode('iso-8859-1'),
                                     encoding='bytes'))
            except (pickle.UnpicklingError, AttributeError):
                logger.debug("Station %d: pickling error" % station_id)
                return [rcodes.RC_PE_PICKLING_ERROR]

            store_data(station_id, cluster, event_list)
            logger.debug("Station %d: succesfully completed" % station_id)
            return [rcodes.RC_OK]


def do_init(configfile):
    """Load configuration and passwords and set up a logger handler

    This function will do one-time initialization.  By using global
    variables, we eliminate the need to reread configuration and passwords
    on every request.

    Configuration is read from the datastore configuation file (usually
    `config.ini`):

    .. include:: ../examples/config.ini
       :literal:

    Station information is read from the `station_list` config variable.
    (`station_list.csv` on frome)

    """
    # set up config
    global config
    try:
        config
    except NameError:
        config = configparser.ConfigParser()
        config.read(configfile)

    # set up logger
    if not logger.handlers:
        file = config.get('General', 'log') + '-wsgi.%d' % os.getpid()
        handler = logging.handlers.TimedRotatingFileHandler(file,
                                                            when='midnight',
                                                            backupCount=14)
        handler.setFormatter(formatter)
        logger.addHandler(handler)
        level = LEVELS.get(config.get('General', 'loglevel'), logging.NOTSET)
        logger.setLevel(level=level)

    # read station list
    global station_list
    try:
        station_list
    except NameError:
        station_list = {}
        with open(config.get('General', 'station_list')) as file:
            reader = csv.reader(file)
            for station in reader:
                if station:
                    num, cluster, password = station
                    num = int(num)
                    station_list[num] = (cluster, password)


def store_data(station_id, cluster, event_list):
    """Store verified event data to temporary storage"""

    logger.debug('Storing data for station %d' % station_id)

    dir = os.path.join(config.get('General', 'data_dir'), 'incoming')
    tmp_dir = os.path.join(config.get('General', 'data_dir'), 'tmp')

    if is_data_suspicious(event_list):
        logger.debug('Event list marked as suspicious.')
        dir = os.path.join(config.get('General', 'data_dir'), 'suspicious')

    file = tempfile.NamedTemporaryFile(dir=tmp_dir, delete=False)
    logger.debug('Filename: %s' % file.name)
    data = {'station_id': station_id, 'cluster': cluster,
            'event_list': event_list}
    pickle.dump(data, file)
    file.close()

    shutil.move(file.name, dir)


def is_data_suspicious(event_list):
    """Check data for suspiciousness

    Suspiciousness, a previously unknown quantum number that may signify
    the actual birth of the universe and the reweaving of past fates into
    current events has come to hunt us and our beloved data.

    Apr 7, 2019 0:00 is the default time after a cold start without GPS signal.
    The DAQ will happily send events even when no GPS signal has been
    acquired (yet). Events with timestamp Apr 7, 2019 are most probably caused
    by no or bad GPS signal. Such events must be eigenstates of suspiciousness.

    """
    for event in event_list:
        if event['header']['datetime'].year < 2019:
            logger.debug('Date < 2019: Timestamp has high suspiciousness.')
            return True
        if event['header']['datetime'].date() == datetime.date(2019, 4, 7):
            logger.debug('Date == Apr 7, 2019: No GPS signal?')
            return True
    return False


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
