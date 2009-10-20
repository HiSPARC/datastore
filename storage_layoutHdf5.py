# To change this template, choose Tools | Templates
# and open the template in the editor.

__author__="dremensk"
__date__ ="$17-sep-2009 9:22:35$"

from fcntl import flock
import csv
import definesHdf5
from numarray import *
import tables
from tables.file import openFile
from tables.nra import *

class HisparcClusters(tables.IsDescription):
	station_id = tables.UInt32Col(pos=1)
        cluster_id = tables.UInt32Col(pos=2)
        password = tables.StringCol(20, pos=3)
	description = tables.StringCol(20, pos=4)
        
class HisparcCICdata(tables.IsDescription):
	event_id = tables.UInt32Col(pos=1)
        station_id = tables.UInt32Col(pos=2)
	time = tables.StringCol(8,pos=3)
	nanoseconds = tables.UInt32Col(pos=4)
        SVR = tables.Int32Col(pos=5)
        GRD = tables.Int32Col(pos=6)
        TR = tables.Int32Col(shape=4,pos=7) #pointer array
        SDT = tables.Int32Col(pos=8)
        GST = tables.Int32Col(pos=9)
        AEN = tables.Int32Col(pos=10)
        GEN = tables.Int32Col(pos=11)
        PH = tables.Float64Col(shape=4,pos=12) #array of double values
        NP = tables.Int32Col(shape=4,pos=13)  # array of integers (Raw number of peaks scintillator)
        BL = tables.Float64Col(shape=4,pos=14) #array of double values
        IN = tables.Float64Col(shape=4,pos=15)
	TRIGPATTERN = tables.Int32Col(pos=16)
	EVENTRATE = tables.Float64Col(pos=17)
	RED = tables.Int32Col(18)
	STDDEV1 = tables.Float64Col(pos=19)
	STDDEV2 = tables.Float64Col(pos=20)
	STDDEV3 = tables.Float64Col(pos=21)
	STDDEV4 = tables.Float64Col(pos=22)
	
class HisparcCMPdata(tables.IsDescription):
        event_id = tables.UInt32Col(pos=1)
        station_id = tables.UInt32Col(pos=2)
	time = tables.StringCol(8,pos=3) 
	nanoseconds = tables.UInt32Col(pos=4)
	CMP_DEVICE = tables.Int32Col(pos=5)
	CMP_COMPARATOR = tables.Int32Col(pos=6)
	CMP_COUNT = tables.Int32Col(pos=7)

class HisparcERRdata(tables.IsDescription):
	event_id = tables.UInt32Col(pos=1)
        station_id = tables.UInt32Col(pos=2)
	time = tables.StringCol(8,pos=3) 
	nanoseconds = tables.UInt32Col(pos=4)
	ERRMSG = tables.Int32Col(pos=5) # POINTER TO ERROR MESSAGE

class HisparcADCdata(tables.IsDescription):
        event_id = tables.UInt32Col(pos=1)
        station_id = tables.UInt32Col(pos=2)
	time = tables.StringCol(8,pos=3) 
	nanoseconds = tables.UInt32Col(pos=4)
        AA2 = tables.Int32Col(pos=5)
        AZ2 = tables.Int32Col(pos=6)
        AV2 = tables.Float64Col(pos=7)
        TI2 = tables.Float64Col(pos=8)
        TA2 = tables.Float64Col(pos=9)
        NS2 = tables.Int32Col(pos=10)
        AI2 = tables.Int32Col(pos=11)
        NS1 = tables.Int32Col(pos=12)
        TA1 = tables.Float64Col(pos=13)
        SVR = tables.Int32Col(pos=14)
        AI1 = tables.Int32Col(pos=15)
        AA1 = tables.Int32Col(pos=16)
        AZ1 = tables.Int32Col(pos=17)
        AV1 = tables.Float64Col(pos=18)
        TI1 = tables.Float64Col(pos=19)

class HisparcGPSdata(tables.IsDescription):
	event_id = tables.Int32Col(pos=1)
        station_id = tables.UInt32Col(pos=2)
	time = tables.StringCol(8,pos=3)
	nanoseconds = tables.UInt32Col(pos=4)
        SNU = tables.StringCol(20)
        GEN = tables.Int32Col()
        GST = tables.Int32Col()
        GHE = tables.Float64Col()
        GLO = tables.Float64Col()
        GLA = tables.Float64Col()
        SVR = tables.Int32Col()
        SST = tables.Int32Col() #BLOB pointer!
        
class HisparcWTRdata(tables.IsDescription):
	event_id = tables.UInt32Col(pos=1)
        station_id = tables.UInt32Col(pos=2)
	time = tables.StringCol(8,pos=3)
	nanoseconds = tables.UInt32Col(pos=4)
        W00 = tables.Float64Col()
        W01 = tables.Float64Col()
        W02 = tables.Float64Col()
        W03 = tables.Float64Col()
        W04 = tables.Float64Col()
        W05 = tables.Float64Col()
        W06 = tables.Float64Col()
        W07 = tables.Float64Col()
        W08 = tables.Float64Col()
        W09 = tables.Float64Col()
        W10 = tables.Float64Col()
        W11 = tables.Float64Col()
        W12 = tables.Float64Col()
        W13 = tables.Float64Col()

def get_clusters(datafile):
    csvFile = csv.reader(open(datafile), delimiter=',', quotechar='"')
    clusters = []
    for row in csvFile:
        clusters.append(row[0])
    return clusters
       
def initialize_clusters(datafile):
    global data_clusters
    data_clusters = tables.openFile(datafile, 'w', 'HiSPARC clusters')
    clustersTable = data_clusters.createTable("/", 'HisparcClusters', HisparcClusters, 'HiSPARC clusters-stations table')

    dataFile = csv.reader(open(definesHdf5.CSV_CLUSTERS), delimiter=",", quotechar='"')
    for r in dataFile: # station, cluster, password, description
        newRow = clustersTable.row
        newRow['station_id'] = r[0]
        newRow['cluster_id'] = r[1]
        newRow['password'] = r[2]
        newRow['description'] = r[3]
        newRow.append()
    data_clusters.flush()
    data_clusters.close()
    
def initialize_database(datafile):
    data = tables.openFile(datafile, 'w', 'HiSPARC data')

    # hisparc/
    hisparc = data.createGroup('/', 'hisparc', 'HiSPARC data')

    clusters = get_clusters(definesHdf5.CSV_CLUSTERS)

    for cluster_id in clusters:
        cluster = data.createGroup(hisparc, "cluster"+(cluster_id), 'HiSPARC cluster '+str(cluster_id))

        # CIC
        CIC = data.createGroup(cluster, "CIC", "HiSPARC Coincidence group" )
        tableCIC = data.createTable(CIC, 'CICEventdata', HisparcCICdata, 'HiSPARC coincidences table')
        tableCIC.attrs.name = "HiSPARC coincidence"
        data.createVLArray(CIC, 'BLOBS', tables.VLStringAtom(),'HiSPARC event traces', filters=tables.Filters(complevel=9))

        # ADC
        ADC = data.createGroup(cluster, "ADC", "HiSPARC ADC group" )
        tableADC = data.createTable(ADC, 'ADCEventdata', HisparcADCdata, 'HiSPARC ADC table')
        tableADC.attrs.name = "HiSPARC ADC settings"
        data.createVLArray(ADC, 'BLOBS', tables.VLStringAtom(),'BLOBS', filters=tables.Filters(complevel=9))

        # GPS
        GPS = data.createGroup(cluster, "GPS", "HiSPARC GPS group" )
        tableGPS = data.createTable(GPS, 'GPSEventdata', HisparcGPSdata, 'HiSPARC GPS table')
        tableGPS.attrs.name="HiSPARC GPS"
        data.createVLArray(GPS, 'BLOBS', tables.VLStringAtom(),'BLOBS', filters=tables.Filters(complevel=9))

        # WTR
        WTR = data.createGroup(cluster, "WTR", "HiSPARC WTR group" )
        tableWTR = data.createTable(WTR, 'WTREventdata', HisparcWTRdata, 'HiSPARC WTR table')
        tableWTR.attrs.name="HiSPARC Weather"
        data.createVLArray(WTR, 'BLOBS', tables.VLStringAtom(),'WTR BLOBS', filters=tables.Filters(complevel=9))

	# ERR
	ERR = data.createGroup(cluster, "ERR", "HiSPARC ERR group" )
	tableERR = data.createTable(ERR, 'ERREventdata', HisparcERRdata, 'HiSPARC ERR table')
        tableERR.attrs.name="HiSPARC ERROR MSGS"
        data.createVLArray(ERR, 'BLOBS', tables.VLStringAtom(),'ERR MSGs', filters=tables.Filters(complevel=9))

	# CMP
	CMP = data.createGroup(cluster, "CMP", "HiSPARC CMP group" )
	tableWTR = data.createTable(CMP, 'CMPEventdata', HisparcCMPdata, 'HiSPARC CMP table')
        tableWTR.attrs.name="HiSPARC Comparisons"
        data.createVLArray(CMP, 'BLOBS', tables.VLStringAtom(),'CMP BLOBS', filters=tables.Filters(complevel=9))

    data.flush()
    data.close()



def open_h5_file(date, mode):
    path= DATA_ROOT_DIR+"/%s/%s/" % (date.year, date.month)
    filename="%s_%s_%s.h5" % (date.year, date.month,date.day)

    try:
            makedirs(path,0777)
    except:
            print "directory %s already exists" % path
    #test if the H5 file actually exists
    if(not access(path+filename,F_OK)):
            initialize_database(path+filename)
            print"file %s/%s was created" % (path,filename)

    #We use a dummy file to lock the actual file
    dummyFile = open(path+filename, mode)
    flock(dummyFile, LOCK_EX)
    #Now once the file is locked, we open the h5handler
    h5handler = openFile(path+filename,mode)
    return [h5handler, dummyFile]



def openDataFile(year, month, day, mode):
	sPath = "./" + definesHdf5.DATA_ROOT_DIR + "/" + str(year) + "/" + str(month) + "/"+str(year)+"_"+str(month)+"_"+str(day)+".h5"
	try:
		dataFile = openFile(sPath, mode)
		#print dataFile
	except IOError:
		print "Cannot open file: %s" % (sPath)
	else:
		return dataFile

