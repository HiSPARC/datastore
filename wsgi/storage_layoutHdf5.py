from fcntl import flock
import csv
import definesHdf5
import tables

class HisparcClusters(tables.IsDescription):
    station_id = tables.UInt32Col(pos=1)
    cluster_id = tables.StringCol(40, pos=2)
    password = tables.StringCol(20, pos=3)
    description = tables.StringCol(20, pos=4)
       
class HisparcEvent(tables.IsDescription):
    # DISCUSS: use of signed (dflt -1) vs unsigned (labview code)
    event_id = tables.UInt32Col(pos=0)
    station_id = tables.UInt16Col(pos=1)
    timestamp = tables.Time32Col(pos=2)
    nanoseconds = tables.UInt32Col(pos=3)
    ext_timestamp = tables.UInt64Col(pos=4)
    data_reduction = tables.BoolCol(pos=5)
    trigger_pattern = tables.UInt32Col(pos=6)
    baseline = tables.Int16Col(shape=4, dflt=-1, pos=7)
    std_dev = tables.Int16Col(shape=4, dflt=-1, pos=8)
    n_peaks = tables.Int16Col(shape=4, dflt=-1, pos=9)
    pulseheights = tables.Int16Col(shape=4, dflt=-1, pos=10)
    integrals = tables.Int32Col(shape=4, dflt=-1, pos=11)
    traces = tables.Int32Col(shape=4, dflt=-1, pos=12)
    event_rate = tables.Float32Col(pos=13)
       
class HisparcError(tables.IsDescription):
    event_id = tables.UInt32Col(pos=0)
    station_id = tables.UInt16Col(pos=1)
    timestamp = tables.Time32Col(pos=2)
    messages = tables.Int32Col(pos=3)

class HisparcComparatorData(tables.IsDescription):
    event_id = tables.UInt32Col(pos=0)
    station_id = tables.UInt16Col(pos=1)
    timestamp = tables.Time32Col(pos=2)
    nanoseconds = tables.UInt32Col(pos=3)
    ext_timestamp = tables.UInt64Col(pos=4)
    device = tables.UInt8Col(pos=5)
    comparator = tables.UInt8Col(pos=6)
    count = tables.UInt16Col(pos=7)

def get_clusters(datafile):
    csvFile = csv.reader(open(datafile), delimiter=',', quotechar='"')
    clusters = set()
    for row in csvFile:
        clusters.add(row[1])
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
    """Initialize the HDF5 file

    This function creates a new HDF5 file with groups for each cluster and
    populates the groups with necessary tables and arrays.

    """
    data = tables.openFile(datafile, 'w', 'HiSPARC data')
    hisparc = data.createGroup('/', 'hisparc', 'HiSPARC data')

    clusters = get_clusters(definesHdf5.CSV_CLUSTERS)

    for cluster_id in clusters:
        cluster = data.createGroup(hisparc,
                                   "cluster_" + cluster_id.lower(),
                                   'HiSPARC cluster ' + cluster_id)
        data.createTable(cluster, 'events', HisparcEvent,
                         'HiSPARC coincidences table')
	data.createTable(cluster, 'errors', HisparcError,
                         'HiSPARC error messages')
	data.createTable(cluster, 'comparator', HisparcComparatorData,
                         'HiSPARC comparator messages')
        data.createVLArray(cluster, 'blobs', tables.VLStringAtom(),
                           'HiSPARC binary data')

    data.flush()
    data.close()
