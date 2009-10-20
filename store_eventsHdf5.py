import sys
import os.path

#import apache
import rcodesHdf5
from definities import *
from rcodesHdf5 import *


#import os
from tables import *
import logging
#import storage_layoutHdf5
from storage_layoutHdf5 import initialize_clusters
import datetime
import random
from os import makedirs, access, F_OK, path
#import fcntl
from fcntl import *
from LockMechanism import *

################################

# Create a logger and set it up.
# NOTE: We implicitly configure the root logger here so that all
#       loggers in the modules will inherit the same settings.
log_fhandler = logging.FileHandler("/tmp/hisparc_upload")
formatter = logging.Formatter("%(asctime)s %(levelname)s %(name)s:%(message)s")
log_fhandler.setFormatter(formatter)
logger = logging.getLogger()logger.name = "main"
logger.addHandler(log_fhandler)
logger.setLevel(logging.INFO)

################################

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
	dataFile = openFile(DATAFILE_CLUSTERS, "r")
	cluster = dataFile.root.HisparcClusters.readWhere(sCondition)
	#print cluster[0][1]
        result = cluster[0][1]
    except IOError:
	print "Cannot open file: %s" % (DATAFILE_CLUSTERS)
        result = -1
        dataFile.flush()
        dataFile.close()
    except IndexError:
        print "No station with such id present in file: %s" % (DATAFILE_CLUSTERS)
        result = -1
        dataFile.flush()
        dataFile.close()
    dataFile.close()
    return result
'''
Stores an event in the h5 filesystem.
@param dataFile- the h5 file in which to store the event
@param eventtype- the type of the event
@param eventheader- the header of the event
@param eventdatalist- the data associated to the event
@param eventGroup- the node in which to store the event in the h5 file
@param station_id- the id of the station this event belongs to
'''
def storeEvent(dataFile, eventtype, eventheader, eventdatalist, eventGroup, station_id):
       # at this point, we were given a event group (eventGroup) in which to store a list of data (eventdatalist)
	try:
		#get a handler to the table in which to insert the new event's data
		eventDataTable = dataFile.getNode(eventGroup, eventtype+'Eventdata')
	except Exception, msg:
		logger.error("\nPROBLEM WHILE OPENING H5FILE : `%s'" % str(msg))
		return RC_PE_TRANS_FAILED
		
	#get the new event ID (size of table + 1 )
	event_id = eventDataTable.nrows + 1

	#prepare the new record
	newRow = eventDataTable.row
	newRow['event_id'] = str(event_id)
	newRow['station_id'] = station_id
	newRow['nanoseconds'] = long(eventheader['nanoseconds'])
	newRow['time'] = eventheader['datetime'].time()

	try:	
		for datalist in eventdatalist:
		    data_uploadcode = datalist['data_uploadcode']
		    logger.info("data type being inserted : `%s'\n" % \
		        str(data_uploadcode))
		    data = datalist['data']
		    # THIS CONDITION SHOULD INCLUDE ALL THE EVENT DATA TYPES CONTAINING A BLOB
		    # IF YOU HAD A NEW EVENT DATA TYPE, BE SURE TO ADD ITS HANDLER HERE
		    if data_uploadcode in ['TR1', 'TR2', 'TR3', 'TR4', 'SST', 'ERRMSG']:
			# DATA NEEDING A POINTER TO A TRACE
			#we insert the blobs associated with the event
			BLOBS = dataFile.getNode(eventGroup, 'BLOBS')
			BLOBS.append(data)
			BLOBS.flush()
			#we store a pointer to this blob in the event table
			trace_idx = len(BLOBS)
			if(data_uploadcode in ['SST', 'ERRMSG']):
			    newRow[data_uploadcode] = trace_idx
			else:
			    nbTr = int(data_uploadcode[2])-1
			    recordSet = newRow['TR']
			    recordSet[nbTr] = trace_idx
			    newRow['TR'] = recordSet
		    elif data_uploadcode[:2] in ['PH', 'IN', 'BL', 'NP']:
			# COLUMNS WITH INNER ARRAY
			nbPh = int(data_uploadcode[2])-1
			recordSet = newRow[data_uploadcode[:2]]
			recordSet[nbPh] = data
			newRow[data_uploadcode[:2]] = recordSet
		    else:
			# THE REST
			newRow[data_uploadcode] = data

		newRow.append()
		eventDataTable.flush()
	except Exception, msg:
		print "**********************************************\n/!\ Problem while inserting event data /!\ \n\t %s\n**********************************************" % msg
		logger.error("\n => PROBLEM WHILE INSERTING EVENT : `%s'       %s " % ( data_uploadcode,msg))
		
		return RC_PE_INV_UPCODE	return RC_OK


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
	print "WRONG PASSWORD:  THE STATION CANNOT SAVE ITS EVENTS"
	return rc
    #previousDate will be used to check if it is the first event in the list
    previousDate = datetime.date(1900,12,12)

    for event in event_list:
	nbEvents += 1
	#logger.info("TREATING THIS EVENT `%s'" % str(event))
        # FIRST, we check the date of the event to insert
        header = event['header']
        datalist = event['datalist']

        dateEvent = event['header']['datetime'].date()
        print dateEvent

        #here we check if the current event's date is different than the previous one
        if dateEvent != previousDate:
            #new event is on a different date
            if previousDate != datetime.date(1900,12,12):
                #not the first event of the list, we need to close the previous file
                #we flush and unlock the file
                close_flush_and_unlock(H5file, dummyFile)
            #we need to open the file to store the event in
            [H5file,dummyFile] = open_h5_file(dateEvent, "a")

        #at this point, H5file is a handler to the h5 file in which the event needs to be inserted
        #we check to which cluster and type this event belongs
  
        # check all subgroups by eventtype_uploadcode
        cluster = get_cluster(station_id)
        clusterName = 'cluster'+str(cluster)
        clusterSubgroup = H5file.getNode("/hisparc/", clusterName)

        # Now we look at what kind of event this is
        eventtype_uploadCode = event['header']['eventtype_uploadcode']
	if not(eventtype_uploadCode == 'CFG'):
		# find the eventtype subgroup within the cluster
		try:
		    eventGroup = H5file.getNode(clusterSubgroup, eventtype_uploadCode)
		except NoSuchNodeError, msg:
		    #the event type is not supported inside the h5 file => we return an error
		    logger.error("\nInvalid eventtype uploadcode: %s msg: %s" %
		                 (header['eventtype_uploadcode'], msg),)
		    close_flush_and_unlock(H5file, dummyFile)
		    return RC_PE_INV_EVENTTYPE

		#Now, we call storeEvent on the correct table, with the correct event type
		result = storeEvent(H5file, eventtype_uploadCode, header, datalist, eventGroup, station_id)
		if( result != RC_OK):
		    # inserting the previous event failed => we break the loop
		    # if the writing failed, we need to close and unlock the file for other threads
		    close_flush_and_unlock(H5file, dummyFile)
		    return result
		previousDate = dateEvent
    #closing file if it was not done before
    close_flush_and_unlock(H5file, dummyFile)
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
	dataFile = openFile(DATAFILE_CLUSTERS, "r")
    	clusterTable = dataFile.root.HisparcClusters
	result = [x['password'] for x in clusterTable.iterrows() if x['station_id']==station_id]
        password = result[0]
       
    except:
        logger.error("\nProblem accessing cluster's h5 file ")
	password = None

    dataFile.close()
    return password




