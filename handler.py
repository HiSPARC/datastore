from mod_python import apache, util
from cPickle import dumps, loads, UnpicklingError
#from store_events import store_event_list, test_db_connection
from store_eventsHdf5 import store_event_list
from rcodesHdf5 import *
from md5_sum import md5_sum
import logging
import sys
import datetime
import traceback

log_fhandler = logging.FileHandler("/tmp/hisparc_uploadHANDLER")
formatter = logging.Formatter("%(asctime)s %(levelname)s %(name)s:%(message)s")
log_fhandler.setFormatter(formatter)
logger = logging.getLogger()
logger.name = "main"
logger.addHandler(log_fhandler)
logger.setLevel(logging.INFO)


def handler(req):
    """ The hisparc upload handler.

    This handler is called by apache whenever someone requests
    http://peene.nikhef.nl/hisparc/*.

    First, we generate a dictionary of POSTed variables and try to read out the
    station_id, password, checksum and data. When we do a req.read(), we
    already read out the entire datastream. I don't know if we can first check
    on station_id/password combinations before reading out the datastream
    without setting up a bidirectional communication channel.

    When the checksum matches, we unpickle the event_list and pass everything
    on to store_event_list.

    """
    qs = req.read()
    vars = util.parse_qsl(qs)
    vars = dict(vars)
    
    # debug code by egbert:
    req.content_type = 'text/html'

    try:
        data = vars['data']
        checksum = vars['checksum']
        station_id = int(vars['station_id'])
        password = vars['password']
    except (KeyError, EOFError):
        returncode = RC_ISE_INV_POSTDATA
    else:
        our_checksum = md5_sum(data)
        

        if our_checksum == checksum:
            try:
                event_list = loads(data)
            except (UnpicklingError, AttributeError):
                returncode = RC_ISE_INV_POSTDATA
                #req.write('debuginfo: RC_ISE_INV_POSTDATA')
            else:
		returncode = '100'
		try:
			#logger.info("\n => SENDING EVENT LIST : `%s'    " % (  event_list))
	                returncode = store_event_list(station_id, password, event_list)
			logger.info("\n => RETURN CODE : `%s' " % ( returncode))
			
		except Exception, msg:
                        logger.error(traceback.format_exc())
                        returncode = RC_PE_TRANS_FAILED
        else:
            returncode = RC_PE_INV_AUTHCODE

    req.write(str(returncode))
    return apache.OK


"""
Reverse engineering protocol structure:

HTTP POST to (in our case) http://localhost/hisparc/handler.py with fields (normal x-www-form-urlencoded as from web pages):
  'data'       : string, python serialized event list, using the 'pickle' library: see http://docs.python.org/library/pickle.html#usage
  'checksum'   : integer, md5 checksum of data
  'station_id' : integer, database id of station from which this data came
  'password'   : string, some password (fixme: what is this?)
  
  the event list (as serialized in field 'data') is structured as follows:
    [
      {
        'header': 
          {
            'eventtype_uploadcode': (string) someEvent.eventtype_uploadcode,
            'date':                 (string) someEvent.datetime.date().isoformat(),
            'time':                 (string) someEvent.datetime.time().isoformat(),
            'nanoseconds':          (int)    someEvent.nanoseconds,
          },
        'datalist': 
          [
            {
              'calculated':      (boolean),
              'data_uploadcode': (string),
              'data':            (string), is base64 encoded iff (data_uploadcode in ['TR1', 'TR2', 'TR3', 'TR4']), otherwise not encoded
            }, 
            ...
          ]
      },
      ...
    ]


"""
