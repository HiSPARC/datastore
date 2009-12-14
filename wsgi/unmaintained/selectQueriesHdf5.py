from numarray import *
from fileSystem import openDataFile
from fileSystem import openDataFilePath
from fileSystem import openAndLockDummyFile
from tables import *
from tables.nra import *
from fileSystem import unlockAndCloseDummyFile
from fileSystem import *

# This file contains the queries needed to retrive data from an HDF5 file
__author__="prmarcu"
__date__ ="$18-sep-2009 11:15:31$"

'''
Returns the table located in the cluster defined by the clusterId.
All this inside of an HDF5 called dataFile.
NOTE: The HDF5 file has to respect the structure defined by OOTI generation 2008-2010
'''
def getTableFromGroup(dataFile,clusterId,groupName,tabelName):
    #get the node with the clusterID
    strClusterID='cluster'+str(clusterId)
    #get the
    clusterGroup=dataFile.getNode('/hisparc/'+strClusterID,groupName)
    #get the table of the given group
    return dataFile.getNode(clusterGroup, tabelName)

'''
Returns the blob array of a specified group
@param dataFile- the opened HDF5 file
@param clusterID- the id of the cluster (an integer)
@param groupName- the name of the group
'''
def getBlobOfGroup(dataFile,clusterId,groupName):
    #get the node with the clusterID
    strClusterID='cluster'+str(clusterId)
    #get the cluster group
    clusterGroup=dataFile.getNode('/hisparc/'+strClusterID,groupName)
    return clusterGroup.BLOBS

'''
Selects all events from a given cluster from a given date
THIS METHOD OPENS AND CLOSES THE FILE
@param datFile- the path to the HDF5 file
@param cluster- the id of the cluster (an integer)
@return a pyTable table object (loaded with data)
'''
def selectClusterEventDayHdf5(dataFile,cluster):
    #get the lock for the dummy file
    fileDummy=openAndLockDummyFile()
    #open the HDF5
    openDataFile=openDataFilePath(dataFile,"r")
    #access the event table the cide us CIC
    tblEvent=getTableFromGroup(openDataFile, cluster, "CIC", "CICEventdata")
    # selecting data
    rows=tblEvent.read()
    #close the HDF5 file
    openDataFile.close()
    #unlock the dummy file
    unlockAndCloseDummyFile(fileDummy)
    return rows

'''
Select the given stations all events for the mentioned day
THIS METHOD OPENS AND CLOSES THE FILE
@param dataFile- the path to the HDF5 file
@param cluster- the id of the cluster (an integer)
@param station the id of the station (an integer)
@return A collection of rows (a table object)
'''
def selectEventStationDay(dataFile, cluster, station):
    #get the lock for the dummy file
    fileDummy = openAndLockDummyFile()
    #open the HDF5
    openDataFile=openDataFilePath(dataFile,"r")
    #access the event table the cide us CIC
    tblEvent=getTableFromGroup(openDataFile, cluster, "CIC", "CICEventdata")
    # selecting data
    sCondition = "station_id == %d" % (station)
    #print "Start query 1 with condition %s" % (sCondition)
    #  count  = 0
    #  for row in tblEvent.where(sCondition):
    #		count += 1
    #		print "%d | % d" % \
    #		(row['event_id'], row['station_id'])
    #  print "Num of rows: %d" % (count)
    #
    #  # close the data file
    #  dataFile.close()`
    rows = tblEvent.readWhere(sCondition)
    #close the HDF5 file
    openDataFile.close()
    #unlock the dummy file
    unlockAndCloseDummyFile(fileDummy)
    return rows

'''
Selects the event that has the ID equal with the ID transmitted as parameter
THIS METHODS OPENS AND CLOSES THE FILE
@param dataFile - the path to the HDF5 file
@param cluster - the ID of the cluster
@param eventID - the ID of the event
@return - a row object correespondig to the selected event
'''
def selectEventByEventID(dataFile, cluster, eventID):
     #get the lock for the dummy file
    fileDummy = openAndLockDummyFile()
    #open the HDF5
    openDataFile = openDataFilePath(dataFile, "r")
    # get the table
    eventTable=getTableFromGroup(openDataFile, cluster, "CIC", "CICEventdata")
    #get the event with the given event ID
    sCondition = "event_id == %d" % (eventID)
    #read from the table the event
    row=eventTable.readWhere(sCondition)
    #lets close the data file
    openDataFile.close()
    #unlock the dummy file
    unlockAndCloseDummyFile(fileDummy)
    # return data
    return row

'''
Selects the trace of the event indicated by the event ID
THIS METHOD OPENS AND CLOSES THE FILE
@param dataFile - the path to the data file
@param cluster - the id of the cluster
@param eventID - the ID of the event
@return - a list of traces associated with the event specified by the eventID
'''
def selectEventTraceData(dataFile,cluster,eventID):
    #get the lock for the dummy file
    fileDummy=openAndLockDummyFile()
    #open the HDF5
    openDataFile=openDataFilePath(dataFile, "r")
    # the blob array
    blobThing=getBlobOfGroup(openDataFile, cluster, "CIC")
    # get the table
    eventTable=getTableFromGroup(openDataFile, cluster, "CIC", "CICEventdata")
    #get the event with the given event ID
    sCondition = "event_id == %d" % (eventID)
    #read from the table the event
    row = eventTable.readWhere(sCondition)
    #the list of traces
    traces=[]

    #fill up the traces
    #every event has max 4 traces; so an event can have 2 or 4 traces

    #the blob is accesed in the following way:
    #in the event table the TR column keeps a list of pointers for the blobs
    #these pointers are simple numbers which indicate the given trace in which
    #row can be found in the BLOBS blob array.
    #The list in the TR column cointains 4 elements (each element of the
    #list(pointer) corresponds to record in the BLOB array.
    rij = row['TR'][0]
    for r in xrange(4):
        if rij[r] > 0:
            traces.append(blobThing[rij[r]-1])
        else:
            traces.append(None)
    #lets close the data file
    openDataFile.close()
    #unlock the dummy file
    unlockAndCloseDummyFile(fileDummy)
    #return the list of trace
    return traces
'''
Selects the PH of the event indicated by the event ID
@param dataFile - the path to the data file
@param cluster - the id of the cluster
@param eventID - the ID of the event
@return - a list of PH associated with the event specified by the eventID
'''
def selectEventPH(dataFile,cluster,eventID):
    #get the lock for the dummy file
    fileDummy=openAndLockDummyFile()
    #open the HDF5
    openDataFile=openDataFilePath(dataFile,"r")
    # get the table
    eventTable=getTableFromGroup(openDataFile, cluster, "CIC", "CICEventdata")
    #get the event with the given event ID
    sCondition = "event_id == %d" % (eventID)
    #read from the table the event
    row=eventTable.readWhere(sCondition)
    #lets close the data file
    openDataFile.close()
    #unlock the dummy file
    unlockAndCloseDummyFile(fileDummy)
    #return the list of trace
    return row['PH'][0]
