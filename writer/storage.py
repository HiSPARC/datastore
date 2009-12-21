import csv
import tables
import os


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

class HisparcConfiguration(tables.IsDescription):
    gps_lat = tables.Float64Col()
    gps_long = tables.Float64Col()
    gps_alt = tables.Float64Col()
    mas_version = tables.Int32Col(dflt=-1)
    slv_version = tables.Int32Col(dflt=-1)
    triglowsig = tables.UInt32Col()
    trighighsig = tables.UInt32Col()
    trigext = tables.UInt32Col()
    trigandor = tables.BoolCol()
    prectime = tables.Float64Col()
    ctime = tables.Float64Col()
    postctime = tables.Float64Col()
    detnum = tables.UInt16Col()
    password = tables.Int32Col(dflt=-1)
    sparebytes = tables.UInt8Col()
    usefilter = tables.BoolCol()
    usefiltthres = tables.BoolCol()
    reduce = tables.BoolCol()
    buffer = tables.Int32Col(dflt=-1)
    startmode = tables.BoolCol()
    delayscreen = tables.Float64Col()
    delaycheck = tables.Float64Col()
    delayerror = tables.Float64Col()
    mas_ch1thrlow = tables.Float64Col()
    mas_ch1thrhigh = tables.Float64Col()
    mas_ch2thrlow = tables.Float64Col()
    mas_ch2thrhigh = tables.Float64Col()
    mas_ch1inttime = tables.Float64Col()
    mas_ch2inttime = tables.Float64Col()
    mas_ch1volt = tables.Float64Col()
    mas_ch2volt = tables.Float64Col()
    mas_ch1curr = tables.Float64Col()
    mas_ch2curr = tables.Float64Col()
    mas_compthrlow = tables.Float64Col()
    mas_compthrhigh = tables.Float64Col()
    mas_maxvolt = tables.Float64Col()
    mas_reset = tables.BoolCol()
    mas_ch1gainpos = tables.UInt8Col()
    mas_ch1gainneg = tables.UInt8Col()
    mas_ch2gainpos = tables.UInt8Col()
    mas_ch2gainneg = tables.UInt8Col()
    mas_ch1offpos = tables.UInt8Col()
    mas_ch1offneg = tables.UInt8Col()
    mas_ch2offpos = tables.UInt8Col()
    mas_ch2offneg = tables.UInt8Col()
    mas_commoff = tables.UInt8Col()
    mas_intvoltage = tables.UInt8Col()
    mas_ch1adcgain = tables.Float64Col()
    mas_ch1adcoff = tables.Float64Col()
    mas_ch2adcgain = tables.Float64Col()
    mas_ch2adcoff = tables.Float64Col()
    mas_ch1compgain = tables.Float64Col()
    mas_ch1compoff = tables.Float64Col()
    mas_ch2compgain = tables.Float64Col()
    mas_ch2compoff = tables.Float64Col()
    slv_ch1thrlow = tables.Float64Col()
    slv_ch1thrhigh = tables.Float64Col()
    slv_ch2thrlow = tables.Float64Col()
    slv_ch2thrhigh = tables.Float64Col()
    slv_ch1inttime = tables.Float64Col()
    slv_ch2inttime = tables.Float64Col()
    slv_ch1volt = tables.Float64Col()
    slv_ch2volt = tables.Float64Col()
    slv_ch1curr = tables.Float64Col()
    slv_ch2curr = tables.Float64Col()
    slv_compthrlow = tables.Float64Col()
    slv_compthrhigh = tables.Float64Col()
    slv_maxvolt = tables.Float64Col()
    slv_reset = tables.BoolCol()
    slv_ch1gainpos = tables.UInt8Col()
    slv_ch1gainneg = tables.UInt8Col()
    slv_ch2gainpos = tables.UInt8Col()
    slv_ch2gainneg = tables.UInt8Col()
    slv_ch1offpos = tables.UInt8Col()
    slv_ch1offneg = tables.UInt8Col()
    slv_ch2offpos = tables.UInt8Col()
    slv_ch2offneg = tables.UInt8Col()
    slv_commoff = tables.UInt8Col()
    slv_intvoltage = tables.UInt8Col()
    slv_ch1adcgain = tables.Float64Col()
    slv_ch1adcoff = tables.Float64Col()
    slv_ch2adcgain = tables.Float64Col()
    slv_ch2adcoff = tables.Float64Col()
    slv_ch1compgain = tables.Float64Col()
    slv_ch1compoff = tables.Float64Col()
    slv_ch2compgain = tables.Float64Col()
    slv_ch2compoff = tables.Float64Col()


def open_or_create_file(data_dir, date):
    """Open an existing file or create a new one

    This function opens an existing PyTables file according to the event
    date.  If the file does not yet exist, a new one is created.

    :param data_dir: the directory containing all data files
    :param date: the event date

    """
    dir = os.path.join(data_dir, '%d/%d' % (date.year, date.month))
    file = os.path.join(dir, '%d_%d_%d.h5' % (date.year, date.month,
                                              date.day))

    if not os.path.exists(dir):
        # create dir and parent dirs with mode rwxr-xr-x
        os.makedirs(dir, 0755)

    return tables.openFile(file, 'a')

def get_or_create_cluster_node(file, cluster):
    """Get an existing cluster node or create a new one

    :param file: the PyTables data file
    :param cluster: the name of the cluster

    """
    try:
        hisparc = file.getNode('/', 'hisparc')
    except tables.NoSuchNodeError:
        hisparc = file.createGroup('/', 'hisparc', 'HiSPARC data')
        file.flush()

    node_name = 'cluster_' + cluster.lower()
    try:
        cluster = file.getNode(hisparc, node_name)
    except tables.NoSuchNodeError:
        cluster = file.createGroup(hisparc, node_name,
                                   'HiSPARC cluster %s data' % cluster)
        file.flush()

    return cluster

def get_or_create_node(file, cluster, node):
    """Get an existing node or create a new one

    :param file: the PyTables data file
    :param cluster: the parent (cluster) node
    :param node: the node (e.g. events, blobs)

    """
    try:
        node = file.getNode(cluster, node)
    except tables.NoSuchNodeError:
        if node == 'events':
            node = file.createTable(cluster, 'events', HisparcEvent,
                                   'HiSPARC coincidences table')
        elif node == 'errors':
            node = file.createTable(cluster, 'errors', HisparcError,
                                    'HiSPARC error messages')
        elif node == 'comparator':
            node = file.createTable(cluster, 'comparator',
                                    HisparcComparatorData,
                                    'HiSPARC comparator messages')
        elif node == 'blobs':
            node = file.createVLArray(cluster, 'blobs',
                                      tables.VLStringAtom(),
                                      'HiSPARC binary data')
        elif node == 'config':
            node = file.createTable(cluster, 'config',
                                    HisparcConfiguration,
                                    'HiSPARC configuration messages')
        file.flush()

    return node
