import hashlib
import urlparse
import cPickle as pickle
import logging
import logging.handlers
import tempfile
import ConfigParser
import csv
import os
import shutil

from rcodes import *

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

    This handler is called by apache using mod_wsgi whenever someone
    requests our URL.

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
    input = environ['wsgi.input'].readline()
    vars = urlparse.parse_qs(input)

    # process POST data
    try:
        data = vars['data'][0]
        checksum = vars['checksum'][0]
        station_id = int(vars['station_id'][0])
        password = vars['password'][0]
    except (KeyError, EOFError):
        logger.debug("POST (vars) error")
        return [str(RC_ISE_INV_POSTDATA)]
    else:
        our_checksum = hashlib.md5(data).hexdigest()
        if our_checksum != checksum:
            logger.debug("Station %d: checksum mismatch" % station_id)
            return [str(RC_PE_INV_AUTHCODE)]
        else:
            try:
                event_list = pickle.loads(data)
            except (pickle.UnpicklingError, AttributeError):
                logger.debug("Station %d: pickling error" % station_id)
                return [str(RC_ISE_INV_POSTDATA)]

    try:
        cluster, station_password = station_list[station_id]
    except KeyError:
        logger.debug("Station %d is unknown" % station_id)
        return [str(RC_PE_INV_STATIONID)]

    if station_password != password:
        logger.debug("Station %d: password mismatch: %s" % (station_id,
                                                            password))
        return [str(RC_PE_INV_AUTHCODE)]
    else:
        store_data(station_id, cluster, event_list)
        logger.debug("Station %d: succesfully completed" % station_id)
        return [str(RC_OK)]

def do_init(configfile):
    """Load configuration and passwords and set up a logger handler

    This function will do one-time initialization.  By using global
    variables, we eliminate the need to reread configuration and passwords
    on every request.

    """
    # set up config
    global config
    try:
        config
    except NameError:
        config = ConfigParser.ConfigParser()
        config.read(configfile)

    # set up logger
    if not logger.handlers:
        file = config.get('General', 'log') + '-wsgi.%d' % os.getpid()
        handler = logging.handlers.TimedRotatingFileHandler(file,
                        when='midnight', backupCount=14)
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

    file = tempfile.NamedTemporaryFile(dir=tmp_dir, delete=False)
    data = {'station_id': station_id, 'cluster': cluster,
            'event_list': event_list}
    pickle.dump(data, file)
    file.close()

    shutil.move(file.name, dir)
