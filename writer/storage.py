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
        file.flush()

    return node
