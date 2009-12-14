import sys
import os.path
import calendar
import base64
import tables
import logging
import datetime

import rcodesHdf5
from rcodesHdf5 import *
from storage_layoutHdf5 import initialize_clusters
from upload_codes import eventtype_upload_codes
from definesHdf5 import *

logger = logging.getLogger('store_events')

global nbEvents
nbEvents = 0
'''
Returns the cluster id associated to the station "station_id"
Returns -1 in case of problem
@param station_id- the id of the station
'''
def get_cluster(station_id):
    sCondition = "station_id == %d" % (station_id)
    try:
	dataFile = tables.openFile(DATAFILE_CLUSTERS, "r")
	cluster = dataFile.root.HisparcClusters.readWhere(sCondition)
	#print cluster[0][1]
        result = cluster[0][1]
    except IOError:
	#print "Cannot open file: %s" % (DATAFILE_CLUSTERS)
        result = -1
    except IndexError:
        #print "No station with such id present in file: %s" % (DATAFILE_CLUSTERS)
        result = -1
    finally:
        dataFile.close()
    return result

def store_event(datafile, eventtype, eventheader, eventdatalist,
                eventgroup, station_id):
    """Stores an event in the h5 filesystem

    :param datafile: the h5 file in which to store the event
    :param eventtype: the type of the event
    :param eventheader: the header of the event
    :param eventdatalist: the data associated to the event
    :param eventgroup: the node in which to store the event in the h5 file
    :param station_id: the id of the station this event belongs to

    """
    upload_codes = eventtype_upload_codes[eventtype]
    table = datafile.getNode(eventgroup,
                             upload_codes['tablename'])
    blobs = datafile.getNode(eventgroup, 'blobs')

    row = table.row
    row['event_id'] = table.nrows + 1
    row['station_id'] = station_id
    # make a unix-like timestamp
    timestamp = calendar.timegm(eventheader['datetime'].utctimetuple())
    nanoseconds = eventheader['nanoseconds']
    # make an extended timestamp, which is the number of nanoseconds since
    # epoch
    ext_timestamp = timestamp * long(1e9) + nanoseconds
    row['timestamp'] = timestamp

    if eventtype == 'CIC' or eventtype == 'CMP':
        # This is a HiSPARC coincidence or comparator message, extended
        # timing information is available
        row['nanoseconds'] = nanoseconds
        row['ext_timestamp'] = ext_timestamp

    # get default values for the data
    data = {}
    for key, value in upload_codes.items():
        if key not in ['tablename', 'blobs']:
            data[key] = row[value]

    # process event data
    for item in eventdatalist:
        # uploadcode: EVENTRATE, PH1, IN3, etc.
        uploadcode = item['data_uploadcode']
        # value: actual data value
        value = item['data']

        if data_is_blob(uploadcode, upload_codes['blobs']):
            # data should be stored inside the blob array, ...
            if uploadcode[:-1] == 'TR':
                # traces are base64 encoded
                value = base64.decodestring(value)
            blobs.append(value)
            # ... with a pointer stored in the event table
            value = len(blobs) - 1

        if uploadcode[-1].isdigit():
            # uploadcode: PH1, IN3, etc.
            key, index = uploadcode[:-1], int(uploadcode[-1]) - 1
            data[key][index] = value
        else:
            # uploadcode: EVENTRATE, RED, etc.
            data[uploadcode] = value

    # write data values to row
    for key, value in upload_codes.items():
        if key not in ['tablename', 'blobs']:
            row[value] = data[key]

    row.append()
    table.flush()
    blobs.flush()

    return RC_OK

def data_is_blob(uploadcode, blob_types):
    """Determine if data is a variable length binary value (blob)"""

    if uploadcode[-1].isdigit():
        if uploadcode[:-1] in blob_types:
            return True
    elif uploadcode in blob_types:
        return True
    return False


'''
Stores a list in the h5 filesystem.
Contains an algorithms that minimizes opening and closing of hdf5 files

@param station_id- the id of the station this list of events belongs to
@param password- the password for this station
@param event_list- the list to process
'''
def store_event_list(station_id, password, event_list):
    #TODO uncomment everything logger related
    #logger.info("Entering store_event_list with event_list for station `%s'" % str(station_id))
    #logger.debug("  I was given %d events" % len(event_list))
    global nbEvents
    rc = check_station_password(station_id, password)
    if rc:
	#print "WRONG PASSWORD:  THE STATION CANNOT SAVE ITS EVENTS"
	return rc
    #previousDate will be used to check if it is the first event in the list
    previousDate = datetime.date(1900,12,12)

    cluster = get_cluster(station_id)
    clusterName = 'cluster_' + cluster.lower()

    for event in event_list:
	nbEvents += 1
	#logger.info("TREATING THIS EVENT `%s'" % str(event))
        # FIRST, we check the date of the event to insert
        header = event['header']
        datalist = event['datalist']

        dateEvent = event['header']['datetime'].date()
        #print dateEvent

        #here we check if the current event's date is different than the previous one
        if dateEvent != previousDate:
            #new event is on a different date
            if previousDate != datetime.date(1900,12,12):
                #not the first event of the list, we need to close the previous file
                #we flush and unlock the file
                LockMechanism.close_flush_and_unlock(H5file, dummyFile)
            #we need to open the file to store the event in
            [H5file,dummyFile] = LockMechanism.open_h5_file(dateEvent, "a")

        #at this point, H5file is a handler to the h5 file in which the event needs to be inserted
        #we check to which cluster and type this event belongs
  
        # check all subgroups by eventtype_uploadcode
        clusterSubgroup = H5file.getNode("/hisparc/", clusterName)

        # Now we look at what kind of event this is
        eventtype_uploadCode = event['header']['eventtype_uploadcode']
	if not(eventtype_uploadCode == 'CFG'):
		# find the eventtype subgroup within the cluster
		try:
		    eventGroup = H5file.getNode(clusterSubgroup)
		except NoSuchNodeError, msg:
		    #the event type is not supported inside the h5 file => we return an error
		    logger.error("\nInvalid eventtype uploadcode: %s msg: %s" %
		                 (header['eventtype_uploadcode'], msg),)
		    close_flush_and_unlock(H5file, dummyFile)
		    return RC_PE_INV_EVENTTYPE

                # Now, we call store_event on the correct table, with the
                # correct event type
                result = store_event(H5file, eventtype_uploadCode, header,
                                     datalist, eventGroup, station_id)
		if( result != RC_OK):
		    # inserting the previous event failed => we break the loop
		    # if the writing failed, we need to close and unlock the file for other threads
		    LockMechanism.close_flush_and_unlock(H5file, dummyFile)
		    return result
		previousDate = dateEvent
    #closing file if it was not done before
    LockMechanism.close_flush_and_unlock(H5file, dummyFile)
    #end of the batch, if we arrived, here, it means everything went fine => return RC_OK
    return RC_OK	


'''
Checks the validity of the password associated with one station
Returns proper error code if the password is not correct
Returns proper error code if the station id is not found inside the stations list

@param station_id- the id of the station this list of events belongs to
@param password- the password for this station
'''
def check_station_password(station_id, password):
    db_password = db_station_password(station_id)
    if not db_password:
        logger.error("\nNo such station_id `%s'." % str(station_id))
        return RC_PE_INV_STATIONID

    elif password != db_password:
        logger.error("\nWrong password for station %d: `%s'" % (station_id,password))
        return RC_PE_INV_AUTHCODE
    return

def db_station_password(station_id):
    sCondition = "station_id == %d" % (station_id)
    # if the clusters file is absent, it will be re created
    if(not access(DATAFILE_CLUSTERS,F_OK)):
	    if(not access(DATA_ROOT_DIR, F_OK)):
            	makedirs(DATA_ROOT_DIR)
            initialize_clusters(DATAFILE_CLUSTERS)

    try:
	dataFile = tables.openFile(DATAFILE_CLUSTERS, "r")
    	clusterTable = dataFile.root.HisparcClusters
	result = [x['password'] for x in clusterTable.iterrows() if x['station_id']==station_id]
        password = result[0]
       
    except:
        logger.error("\nProblem accessing cluster's h5 file ")
	password = None

    dataFile.close()
    return password




