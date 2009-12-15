# To change this template, choose Tools | Templates
# and open the template in the editor.

__author__="rladan"
__date__ ="$22-sep-2009 11:31:17$"

DB_HOST = "binladan.teeselink.nl"
DB_USER = "hisparc"
DB_PASSWORD = "Crapsih"
DB_NAME = "hisparc-full"

from storage_layoutHdf5 import initialize_database
from fileSystem import *
from storage_layoutHdf5 import *
from store_eventsHdf5 import *
import MySQLdb
import tables
import os
import csv

def get_db_connection(host=DB_HOST, user=DB_USER, password=DB_PASSWORD, name=DB_NAME):
    # open the database connection, using either supplied or default values
    # works
    src_conn = MySQLdb.connect(host, user, password, name)
    return src_conn

def readclusters():
    # read in the station -> cluster map
    # works
    m = {}
    try:
        dataFile = csv.reader(open(definesHdf5.CSV_CLUSTERS), delimiter=",", quotechar='"')
        for r in dataFile: # station, cluster, password, description
            m[r[0]] = r[1]
    except IOError:
        print "Cannot open file:", definesHdf5.CSV_CLUSTERS
    return m

def migrate(conn):
    # read the MySQL table, keeping the event table as the master table
    # input tables: event, calculateddata(calculateddatatype,eventtype), eventdata(eventdatatype,eventtype)
    # also creates the HDF5 files

    # output tables: root/hisparc/clusterX/
    #   GPS
    #       BLOBS
    #       GPSEventdata(event_id, station_id, time, nanoseconds, GEN, GHE, GLA, GLO, GST, SNU, SST, SVR)
    #   ADC
    #       BLOBS
    #       ADCEventdata(event_id, station_id, time, nanoseconds, AA2, AZ2, AV2, TI2, TA2, NS2, AI2, NS1, TA1, SVR, AI1, AA1, AZ1, AV1, TI1)
    #   WTR
    #       BLOBS
    #       WTREventdata(event_id, station_id, time, nanoseconds, W00-W13)
    #   CIC
    #       BLOBS
    #       CICEventdata(event_id, station_id, time, nanoseconds, SVR, GRD, TR[1-4], SDT, GST, AEN, GEN, PH[1-4], NP[1-4], BL[1-4], IN[1-4])
    #   ERR
    #       BLOBS
    #       ERREventdata(event_id, station_id, time, nanoseconds, ERRMSG) (ERRMSG is blob pointer)
    #   CMP (no blobs)
    #       CMPEventdata(event_id, station_id, time, nanoseconds, CMP_DEVICE, CMP_COMPARATOR, CMP_COUNT)

    oldyear = oldmonth = oldday = 0
    cursor = conn.cursor()
    cursor_ed = conn.cursor()
    cursor_edt = conn.cursor()
    cursor_cd = conn.cursor()
    cursor_cdt = conn.cursor()
    cursor_et = conn.cursor()
    start = 0

    while True:
        cursor.execute("SELECT * FROM event LIMIT %s,1000" % (start,))#returns in batches of MAX 1000 items because MySQL cannot stream data
        # get current row of event table
        events = cursor.fetchall()
        if events == None:
            print "** MIGRATION FINISHED **"
            break
        for event in events:
            _event_id, _station_id, _eventtype_id, _date, _time, _nanoseconds = event
            year = int(str(_date)[:4])
            month = int(str(_date)[5:7])
            day = int(str(_date)[8:])
            print "Event", _event_id, "at", year, month, day

            # date change?
            if oldday != day or oldmonth != month or oldyear != year:
                # see if there is a file for yesterday
                hdf5name = "./" + definesHdf5.DATA_ROOT_DIR + "/" + str(oldyear) + "/" + str(oldmonth) + "/"+str(oldyear)+"_"+str(oldmonth)+"_"+str(oldday)+".h5"
                if os.path.isfile(hdf5name):
                    print "CLOSING OLD FILE"
                    hdf5file.close()
                # new hdf5 file for today
                try:
                    os.makedirs("./" + definesHdf5.DATA_ROOT_DIR + "/" + str(year) + "/" + str(month))
                except OSError, errno:
                    if errno == 17:
                        pass # please continue
                hdf5name = "./" + definesHdf5.DATA_ROOT_DIR + "/" + str(year) + "/" + str(month) + "/"+str(year)+"_"+str(month)+"_"+str(day)+".h5"
                print "INITIALIZING", hdf5name,
                if not os.path.isfile(hdf5name):
                    initialize_database(hdf5name)
                    print "(new)",
                hdf5file = tables.openFile(hdf5name, "r+")
                print "DONE"

            # get the uploadcode (table name)
            cursor_et.execute("SELECT uploadcode FROM eventtype WHERE eventtype_id = %s" % (_eventtype_id,))# exactly 1 result
            (tablename,) = cursor_et.fetchone()
            if not tablename in ["CIC", "ADC", "GPS", "WTR", "CMP", "ERR"]:
                print "Skipping unknown table name", tablename
                continue
            # get the table
            clusterSubgroup = hdf5file.getNode("/hisparc", 'cluster'+str(clusterMap[_station_id]))
            eventGroup = hdf5file.getNode(clusterSubgroup, tablename)
            eventDataTable = hdf5file.getNode(eventGroup, tablename+'Eventdata')
            eventDataRow = eventDataTable.row

            # process the eventdata related to this event
            cursor_ed.execute("SELECT * FROM eventdata WHERE event_id = %s" % (_event_id,))# "small" number
            while True:
                eventdata = cursor_ed.fetchone()
                if eventdata == None:
                    break
                # the eventdata belong to event event_id are put in columns eventdatatype[eventdatatype_id].uploadcode
                ed_eventdatatype_id, _, ed_integervalue, ed_doublevalue, ed_textvalue, ed_blobvalue = eventdata
                cursor_edt.execute("SELECT uploadcode FROM eventdatatype WHERE eventtype_id = %s" % (ed_eventdatatype_id,)) # exactly 1 result
                (columnname,) = cursor_edt.fetchone()
                if not columnname in ["GEN", "GHE", "GLA", "GLO", "GST", "GRD", "SDT", "SNU", "SST", "SVR", "AA1", "AA2", "AI1", "AI2", "AV1", "AV2", "AZ1", "AZ2", "NS1", "NS2", "TA1", "TA2", "TI1", "TI2", "TRIGPATTERN", "EVENTRATE", "RED", "CMP_DEVICE", "CMP_COMPARATOR", "CMP_COUNT", "ERRMSG"]:
                    print "Skipping unknown column name", columnname
                    continue
                # one event has multiple int/double/text/blob values (exclusively)
                if ed_integervalue != None:
                    val = ed_integervalue
                elif ed_doublevalue != None:
                    val = ed_doublevalue
                elif ed_textvalue != None:
                    val = ed_textvalue
                elif ed_blobvalue != None:
                    val = ed_blobvalue #put it in the BLOBS structure
                print "** eventdata: storing", val, "in column", columnnname, "in table", tablename,"with", _event_id, _station_id, _time, _nanoseconds#
                eventDataRow["event_id"] = _event_id
                eventDataRow["station_id"] = _station_id
                eventDataRow["time"] = _time
                eventDataRow["nanoseconds"] = _nanoseconds
                if columname in ["SST", "ERRMSG"]:
                    #we insert the blobs associated with the event
                    BLOBS = hdf5file.getNode(eventGroup, 'BLOBS')
                    BLOBS.append(val)
                    BLOBS.flush()
                    #we store a pointer to this blob in the event table
                    val = len(BLOBS)
                eventDataRow[columnname] = val
                eventDataRow.append()

            # process the calculateddata related to this event
            cursor_cd.execute("SELECT * FROM calculateddata WHERE event_id = %s" % (_event_id,)) # "small" number
            while True:
                calculateddata = cursor_cd.fetchone()
                if calculateddata == None:
                    break
                # the calculateddata belonging to event event_id are put in columnns calculateddatatype[calculateddatatype_id].uploadcode
                cd_calculateddatatype_id, _, cd_integervalue, cd_doublevalue = calculateddata
                cursor_cdt.execute("SELECT uploadcode FROM calculateddatatype WHERE calculateddatatype_id = %s" % (cd_calculateddatatype_id,)) # exactly 1 result
                (columnname,) = cursor_cdt.fetchone()
                if not columnname in ["PH1", "PH2", "PH3", "PH4", "IN1", "IN2", "IN3", "IN4", "BL1", "BL2", "BL3", "BL4", "NP1", "NP2", "NP3", "NP4", "W00", "W01", "W02", "W03", "W04", "W05", "W06", "W07", "W08", "W09", "W10", "W11", "W12", "W13", "STDDEV1", "STDDEV2", "STDDEV3", "STDDEV4"]:
                    print "Skipping unknown column name", columnname
                    continue
                # one calculateddata has multiple int/double values (exclusively)
                if cd_integervalue != None:
                    val = cd_integervalue
                else:
                    val = cd_doublevalue
                print "** calculateddata: storing", val, "in column", columnname, "in table", tablename,"with", _event_id, _station_id, _time, _nanoseconds#
                eventDataRow["event_id"] = _event_id
                eventDataRow["station_id"] = _station_id
                eventDataRow["time"] = _time
                eventDataRow["nanoseconds"] = _nanoseconds
                if columnname[0] != "W":
                    colName = columnname[:2]
                    colNum = int(columnname[2])-1
                    if colName == "TR":
                        #we insert the blobs associated with the event
                        BLOBS = hdf5file.getNode(eventGroup, 'BLOBS')
                        BLOBS.append(val)
                        BLOBS.flush()
                        #we store a pointer to this blob in the event table
                        val = len(BLOBS)
                    # update 4-tuple
                    recordSet = eventDataRow[colName]
                    recordSet[colNum] = val
                    eventDataRow[colName] = recordSet
                else:
                    # normal column
                    eventDataRow[columnname] = val
                eventDataRow.append()

            eventDataTable.flush()
            # next event
            oldyear = year
            oldmonth = month
            oldday = day
        # current batch done
        start += 1000

if __name__ == "__main__":
    global conn, clusterMap
    conn = get_db_connection()
    clusterMap = readclusters()
    migrate(conn)
