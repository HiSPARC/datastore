import csv
import tables
import os


class HisparcClusters(tables.IsDescription):
    station_id = tables.UInt32Col(pos=0)
    cluster_id = tables.StringCol(40, pos=1)
    password = tables.StringCol(20, pos=2)
    description = tables.StringCol(20, pos=3)


class HisparcEvent(tables.IsDescription):
    # DISCUSS: use of signed (dflt -1) vs unsigned (labview code)
    event_id = tables.UInt32Col(pos=0)
    timestamp = tables.Time32Col(pos=1)
    nanoseconds = tables.UInt32Col(pos=2)
    ext_timestamp = tables.UInt64Col(pos=3)
    data_reduction = tables.BoolCol(pos=4)
    trigger_pattern = tables.UInt32Col(pos=5)
    baseline = tables.Int16Col(shape=4, dflt=-1, pos=6)
    std_dev = tables.Int16Col(shape=4, dflt=-1, pos=7)
    n_peaks = tables.Int16Col(shape=4, dflt=-1, pos=8)
    pulseheights = tables.Int16Col(shape=4, dflt=-1, pos=9)
    integrals = tables.Int32Col(shape=4, dflt=-1, pos=10)
    traces = tables.Int32Col(shape=4, dflt=-1, pos=11)
    event_rate = tables.Float32Col(pos=12)


class HisparcError(tables.IsDescription):
    event_id = tables.UInt32Col(pos=0)
    timestamp = tables.Time32Col(pos=2)
    messages = tables.Int32Col(dflt=-1, pos=3)


class HisparcConfiguration(tables.IsDescription):
    event_id = tables.UInt32Col()
    timestamp = tables.Time32Col()
    gps_latitude = tables.Float64Col()
    gps_longitude = tables.Float64Col()
    gps_altitude = tables.Float64Col()
    mas_version = tables.Int32Col(dflt=-1)
    slv_version = tables.Int32Col(dflt=-1)
    trig_low_signals = tables.UInt32Col()
    trig_high_signals = tables.UInt32Col()
    trig_external = tables.UInt32Col()
    trig_and_or = tables.BoolCol()
    precoinctime = tables.Float64Col()
    coinctime = tables.Float64Col()
    postcoinctime = tables.Float64Col()
    detnum = tables.UInt16Col()
    password = tables.Int32Col(dflt=-1)
    spare_bytes = tables.UInt8Col()
    use_filter = tables.BoolCol()
    use_filter_threshold = tables.BoolCol()
    reduce_data = tables.BoolCol()
    buffer = tables.Int32Col(dflt=-1)
    startmode = tables.BoolCol()
    delay_screen = tables.Float64Col()
    delay_check = tables.Float64Col()
    delay_error = tables.Float64Col()
    mas_ch1_thres_low = tables.Float64Col()
    mas_ch1_thres_high = tables.Float64Col()
    mas_ch2_thres_low = tables.Float64Col()
    mas_ch2_thres_high = tables.Float64Col()
    mas_ch1_inttime = tables.Float64Col()
    mas_ch2_inttime = tables.Float64Col()
    mas_ch1_voltage = tables.Float64Col()
    mas_ch2_voltage = tables.Float64Col()
    mas_ch1_current = tables.Float64Col()
    mas_ch2_current = tables.Float64Col()
    mas_comp_thres_low = tables.Float64Col()
    mas_comp_thres_high = tables.Float64Col()
    mas_max_voltage = tables.Float64Col()
    mas_reset = tables.BoolCol()
    mas_ch1_gain_pos = tables.UInt8Col()
    mas_ch1_gain_neg = tables.UInt8Col()
    mas_ch2_gain_pos = tables.UInt8Col()
    mas_ch2_gain_neg = tables.UInt8Col()
    mas_ch1_offset_pos = tables.UInt8Col()
    mas_ch1_offset_neg = tables.UInt8Col()
    mas_ch2_offset_pos = tables.UInt8Col()
    mas_ch2_offset_neg = tables.UInt8Col()
    mas_common_offset = tables.UInt8Col()
    mas_internal_voltage = tables.UInt8Col()
    mas_ch1_adc_gain = tables.Float64Col()
    mas_ch1_adc_offset = tables.Float64Col()
    mas_ch2_adc_gain = tables.Float64Col()
    mas_ch2_adc_offset = tables.Float64Col()
    mas_ch1_comp_gain = tables.Float64Col()
    mas_ch1_comp_offset = tables.Float64Col()
    mas_ch2_comp_gain = tables.Float64Col()
    mas_ch2_comp_offset = tables.Float64Col()
    slv_ch1_thres_low = tables.Float64Col()
    slv_ch1_thres_high = tables.Float64Col()
    slv_ch2_thres_low = tables.Float64Col()
    slv_ch2_thres_high = tables.Float64Col()
    slv_ch1_inttime = tables.Float64Col()
    slv_ch2_inttime = tables.Float64Col()
    slv_ch1_voltage = tables.Float64Col()
    slv_ch2_voltage = tables.Float64Col()
    slv_ch1_current = tables.Float64Col()
    slv_ch2_current = tables.Float64Col()
    slv_comp_thres_low = tables.Float64Col()
    slv_comp_thres_high = tables.Float64Col()
    slv_max_voltage = tables.Float64Col()
    slv_reset = tables.BoolCol()
    slv_ch1_gain_pos = tables.UInt8Col()
    slv_ch1_gain_neg = tables.UInt8Col()
    slv_ch2_gain_pos = tables.UInt8Col()
    slv_ch2_gain_neg = tables.UInt8Col()
    slv_ch1_offset_pos = tables.UInt8Col()
    slv_ch1_offset_neg = tables.UInt8Col()
    slv_ch2_offset_pos = tables.UInt8Col()
    slv_ch2_offset_neg = tables.UInt8Col()
    slv_common_offset = tables.UInt8Col()
    slv_internal_voltage = tables.UInt8Col()
    slv_ch1_adc_gain = tables.Float64Col()
    slv_ch1_adc_offset = tables.Float64Col()
    slv_ch2_adc_gain = tables.Float64Col()
    slv_ch2_adc_offset = tables.Float64Col()
    slv_ch1_comp_gain = tables.Float64Col()
    slv_ch1_comp_offset = tables.Float64Col()
    slv_ch2_comp_gain = tables.Float64Col()
    slv_ch2_comp_offset = tables.Float64Col()


class HisparcComparator(tables.IsDescription):
    event_id = tables.UInt32Col(pos=0)
    timestamp = tables.Time32Col(pos=1)
    nanoseconds = tables.UInt32Col(pos=2)
    ext_timestamp = tables.UInt64Col(pos=3)
    device = tables.UInt8Col(pos=4)
    comparator = tables.UInt8Col(pos=5)
    count = tables.UInt16Col(pos=6)


class WeatherEvent(tables.IsDescription):
    event_id = tables.UInt32Col(pos=0)
    timestamp = tables.Time32Col(pos=1)
    temp_inside = tables.Float32Col(pos=2)
    temp_outside = tables.Float32Col(pos=3)
    humidity_inside = tables.Int16Col(pos=4)
    humidity_outside = tables.Int16Col(pos=5)
    barometer = tables.Float32Col(pos=6)
    wind_dir = tables.Int16Col(pos=7)
    wind_speed = tables.Int16Col(pos=8)
    solar_rad = tables.Int16Col(pos=9)
    uv = tables.Int16Col(pos=10)
    evapotranspiration = tables.Float32Col(pos=11)
    rain_rate = tables.Float32Col(pos=12)
    heat_index = tables.Int16Col(pos=13)
    dew_point = tables.Float32Col(pos=14)
    wind_chill = tables.Float32Col(pos=15)


class WeatherError(tables.IsDescription):
    event_id = tables.UInt32Col(pos=0)
    timestamp = tables.Time32Col(pos=1)
    messages = tables.Int32Col(dflt=-1, pos=2)


class WeatherConfig(tables.IsDescription):
    event_id = tables.UInt32Col(pos=0)
    timestamp = tables.Time32Col(pos=1)
    com_port = tables.UInt8Col(pos=2)
    baud_rate = tables.Int16Col(pos=3)
    station_id = tables.UInt32Col(pos=4)
    database_name = tables.Int32Col(dflt=-1, pos=5)
    help_url = tables.Int32Col(dflt=-1, pos=6)
    daq_mode = tables.BoolCol(pos=7)
    latitude = tables.Float64Col(pos=8)
    longitude = tables.Float64Col(pos=9)
    temperature_inside = tables.BoolCol(pos=10)
    temperature_outside = tables.BoolCol(pos=11)
    humidity_inside = tables.BoolCol(pos=12)
    humidity_outside = tables.BoolCol(pos=13)
    barometer = tables.BoolCol(pos=14)
    wind_direction = tables.BoolCol(pos=15)
    wind_speed = tables.BoolCol(pos=16)
    solar_radiation = tables.BoolCol(pos=17)
    uv_index = tables.BoolCol(pos=18)
    evapotranspiration = tables.BoolCol(pos=19)
    rain_rate = tables.BoolCol(pos=20)
    heat_index = tables.BoolCol(pos=21)
    dew_point = tables.BoolCol(pos=22)
    wind_chill = tables.BoolCol(pos=23)
    offset_inside_temperature = tables.Float32Col(pos=24)
    offset_outside_temperature = tables.Float32Col(pos=25)
    offset_inside_humidity = tables.Int16Col(pos=26)
    offset_outside_humidity = tables.Int16Col(pos=27)
    offset_wind_direction = tables.Int16Col(pos=28)
    offset_station_altitude = tables.Float32Col(pos=29)
    offset_bar_sea_level = tables.Float32Col(pos=30)
    altitude = tables.Float64Col(pos=31)


class LightningEvent(tables.IsDescription):
    event_id = tables.UInt32Col(pos=0)
    timestamp = tables.Time32Col(pos=1)
    corr_distance = tables.Int16Col(pos=2)
    uncorr_distance = tables.Int16Col(pos=3)
    uncorr_angle = tables.Float32Col(pos=4)
    corr_angle = tables.Float32Col(pos=5)


class LightningError(tables.IsDescription):
    event_id = tables.UInt32Col(pos=0)
    timestamp = tables.Time32Col(pos=1)
    messages = tables.Int32Col(dflt=-1, pos=2)


class LightningConfig(tables.IsDescription):
    event_id = tables.UInt32Col(pos=0)
    timestamp = tables.Time32Col(pos=1)
    # FIXME
    # Figure out what config settings the lightning daq will have and input here


class LightningStatus(tables.IsDescription):
    event_id = tables.UInt32Col(pos=0)
    timestamp = tables.Time32Col(pos=1)
    close_rate = tables.Int16Col(pos=2)
    total_rate = tables.Int16Col(pos=3)
    close_alarm = tables.BoolCol(pos=4)
    sever_alarm = tables.BoolCol(pos=5)
    current_heading = tables.Float32Col(pos=6)


class LightningNoise(tables.IsDescription):
    event_id = tables.UInt32Col(pos=0)
    timestamp = tables.Time32Col(pos=1)


def open_or_create_file(data_dir, date):
    """Open an existing file or create a new one

    This function opens an existing PyTables file according to the event
    date.  If the file does not yet exist, a new one is created.

    :param data_dir: the directory containing all data files
    :param date: the event date

    """
    dir = os.path.join(data_dir, '%d/%d' % (date.year, date.month))
    file = os.path.join(dir, '%d_%d_%d.h5' % (date.year, date.month, date.day))

    if not os.path.exists(dir):
        # create dir and parent dirs with mode rwxr-xr-x
        os.makedirs(dir, 0755)

    return tables.openFile(file, 'a')


def get_or_create_station_group(file, cluster, station_id):
    """Get an existing station group or create a new one

    :param file: the PyTables data file
    :param cluster: the name of the cluster
    :param station_id: the station number

    """
    cluster = get_or_create_cluster_group(file, cluster)
    node_name = 'station_%d' % station_id
    try:
        station = file.getNode(cluster, node_name)
    except tables.NoSuchNodeError:
        station = file.createGroup(cluster, node_name,
                                   'HiSPARC station %d data' % station_id)
        file.flush()

    return station


def get_or_create_cluster_group(file, cluster):
    """Get an existing cluster group or create a new one

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
        elif node == 'config':
            node = file.createTable(cluster, 'config', HisparcConfiguration,
                                    'HiSPARC configuration messages')
        elif node == 'comparator':
            node = file.createTable(cluster, 'comparator', HisparcComparator,
                                    'HiSPARC comparator messages')
        elif node == 'blobs':
            node = file.createVLArray(cluster, 'blobs', tables.VLStringAtom(),
                                      'HiSPARC binary data')
        elif node == 'weather':
            node = file.createTable(cluster, 'weather', WeatherEvent,
                                    'HiSPARC weather data')
        elif node == 'weather_errors':
            node = file.createTable(cluster, 'weather_errors', WeatherError,
                                    'HiSPARC weather error messages')
        elif node == 'weather_config':
            node = file.createTable(cluster, 'weather_config', WeatherConfig,
                                    'HiSPARC weather configuration messages')
        elif node == 'lightning':
            node = file.createTable(cluster, 'lightning', LightningEvent,
                                    'HiSPARC lightning data')
        elif node == 'lightning_errors':
            node = file.createTable(cluster, 'lightning_errors', LightningError,
                                    'HiSPARC lightning error messages')
        elif node == 'lightning_config':
            node = file.createTable(cluster, 'lightning_config', LightningError,
                                    'HiSPARC lightning configuration messages')
        elif node == 'lightning_status':
            node = file.createTable(cluster, 'lightning_status', LightningError,
                                    'HiSPARC lightning status messages')
        elif node == 'lightning_noise':
            node = file.createTable(cluster, 'lightning_noise', LightningError,
                                    'HiSPARC lightning noise messages')
        file.flush()

    return node
