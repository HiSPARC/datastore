"""Storage docstrings"""

import tables


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
    """HiSPARC Error messages tables"""

    event_id = tables.UInt32Col(pos=0)
    timestamp = tables.Time32Col(pos=1)
    messages = tables.Int32Col(dflt=-1, pos=2)


class HisparcConfiguration(tables.IsDescription):
    event_id = tables.UInt32Col(pos=0)
    timestamp = tables.Time32Col(pos=1)
    gps_latitude = tables.Float64Col(pos=2)
    gps_longitude = tables.Float64Col(pos=3)
    gps_altitude = tables.Float64Col(pos=4)
    mas_version = tables.Int32Col(dflt=-1, pos=5)
    slv_version = tables.Int32Col(dflt=-1, pos=6)
    trig_low_signals = tables.UInt32Col(pos=7)
    trig_high_signals = tables.UInt32Col(pos=8)
    trig_external = tables.UInt32Col(pos=9)
    trig_and_or = tables.BoolCol(pos=10)
    precoinctime = tables.Float64Col(pos=11)
    coinctime = tables.Float64Col(pos=12)
    postcoinctime = tables.Float64Col(pos=13)
    detnum = tables.UInt16Col(pos=14)
    password = tables.Int32Col(dflt=-1, pos=15)
    spare_bytes = tables.UInt8Col(pos=16)
    use_filter = tables.BoolCol(pos=17)
    use_filter_threshold = tables.BoolCol(pos=18)
    reduce_data = tables.BoolCol(pos=19)
    buffer = tables.Int32Col(dflt=-1, pos=20)
    startmode = tables.BoolCol(pos=21)
    delay_screen = tables.Float64Col(pos=22)
    delay_check = tables.Float64Col(pos=23)
    delay_error = tables.Float64Col(pos=24)
    mas_ch1_thres_low = tables.Float64Col(pos=25)
    mas_ch1_thres_high = tables.Float64Col(pos=26)
    mas_ch2_thres_low = tables.Float64Col(pos=27)
    mas_ch2_thres_high = tables.Float64Col(pos=28)
    mas_ch1_inttime = tables.Float64Col(pos=29)
    mas_ch2_inttime = tables.Float64Col(pos=30)
    mas_ch1_voltage = tables.Float64Col(pos=31)
    mas_ch2_voltage = tables.Float64Col(pos=32)
    mas_ch1_current = tables.Float64Col(pos=33)
    mas_ch2_current = tables.Float64Col(pos=34)
    mas_comp_thres_low = tables.Float64Col(pos=35)
    mas_comp_thres_high = tables.Float64Col(pos=36)
    mas_max_voltage = tables.Float64Col(pos=37)
    mas_reset = tables.BoolCol(pos=38)
    mas_ch1_gain_pos = tables.UInt8Col(pos=39)
    mas_ch1_gain_neg = tables.UInt8Col(pos=40)
    mas_ch2_gain_pos = tables.UInt8Col(pos=41)
    mas_ch2_gain_neg = tables.UInt8Col(pos=42)
    mas_ch1_offset_pos = tables.UInt8Col(pos=43)
    mas_ch1_offset_neg = tables.UInt8Col(pos=44)
    mas_ch2_offset_pos = tables.UInt8Col(pos=45)
    mas_ch2_offset_neg = tables.UInt8Col(pos=46)
    mas_common_offset = tables.UInt8Col(pos=47)
    mas_internal_voltage = tables.UInt8Col(pos=48)
    mas_ch1_adc_gain = tables.Float64Col(pos=49)
    mas_ch1_adc_offset = tables.Float64Col(pos=50)
    mas_ch2_adc_gain = tables.Float64Col(pos=51)
    mas_ch2_adc_offset = tables.Float64Col(pos=52)
    mas_ch1_comp_gain = tables.Float64Col(pos=53)
    mas_ch1_comp_offset = tables.Float64Col(pos=54)
    mas_ch2_comp_gain = tables.Float64Col(pos=55)
    mas_ch2_comp_offset = tables.Float64Col(pos=56)
    slv_ch1_thres_low = tables.Float64Col(pos=57)
    slv_ch1_thres_high = tables.Float64Col(pos=58)
    slv_ch2_thres_low = tables.Float64Col(pos=59)
    slv_ch2_thres_high = tables.Float64Col(pos=60)
    slv_ch1_inttime = tables.Float64Col(pos=61)
    slv_ch2_inttime = tables.Float64Col(pos=62)
    slv_ch1_voltage = tables.Float64Col(pos=63)
    slv_ch2_voltage = tables.Float64Col(pos=64)
    slv_ch1_current = tables.Float64Col(pos=65)
    slv_ch2_current = tables.Float64Col(pos=66)
    slv_comp_thres_low = tables.Float64Col(pos=67)
    slv_comp_thres_high = tables.Float64Col(pos=68)
    slv_max_voltage = tables.Float64Col(pos=69)
    slv_reset = tables.BoolCol(pos=70)
    slv_ch1_gain_pos = tables.UInt8Col(pos=71)
    slv_ch1_gain_neg = tables.UInt8Col(pos=72)
    slv_ch2_gain_pos = tables.UInt8Col(pos=73)
    slv_ch2_gain_neg = tables.UInt8Col(pos=74)
    slv_ch1_offset_pos = tables.UInt8Col(pos=75)
    slv_ch1_offset_neg = tables.UInt8Col(pos=76)
    slv_ch2_offset_pos = tables.UInt8Col(pos=77)
    slv_ch2_offset_neg = tables.UInt8Col(pos=78)
    slv_common_offset = tables.UInt8Col(pos=79)
    slv_internal_voltage = tables.UInt8Col(pos=80)
    slv_ch1_adc_gain = tables.Float64Col(pos=81)
    slv_ch1_adc_offset = tables.Float64Col(pos=82)
    slv_ch2_adc_gain = tables.Float64Col(pos=83)
    slv_ch2_adc_offset = tables.Float64Col(pos=84)
    slv_ch1_comp_gain = tables.Float64Col(pos=85)
    slv_ch1_comp_offset = tables.Float64Col(pos=86)
    slv_ch2_comp_gain = tables.Float64Col(pos=87)
    slv_ch2_comp_offset = tables.Float64Col(pos=88)


class HisparcComparator(tables.IsDescription):
    event_id = tables.UInt32Col(pos=0)
    timestamp = tables.Time32Col(pos=1)
    nanoseconds = tables.UInt32Col(pos=2)
    ext_timestamp = tables.UInt64Col(pos=3)
    device = tables.UInt8Col(pos=4)
    comparator = tables.UInt8Col(pos=5)
    count = tables.UInt16Col(pos=6)


class HisparcSingle(tables.IsDescription):
    event_id = tables.UInt32Col(pos=0)
    timestamp = tables.Time32Col(pos=1)
    mas_ch1_low = tables.Int32Col(dflt=-1, pos=2)
    mas_ch1_high = tables.Int32Col(dflt=-1, pos=3)
    mas_ch2_low = tables.Int32Col(dflt=-1, pos=4)
    mas_ch2_high = tables.Int32Col(dflt=-1, pos=5)
    slv_ch1_low = tables.Int32Col(dflt=-1, pos=6)
    slv_ch1_high = tables.Int32Col(dflt=-1, pos=7)
    slv_ch2_low = tables.Int32Col(dflt=-1, pos=8)
    slv_ch2_high = tables.Int32Col(dflt=-1, pos=9)


class HisparcSatellite(tables.IsDescription):
    event_id = tables.UInt32Col(pos=0)
    timestamp = tables.Time32Col(pos=1)
    min_n = tables.UInt16Col(pos=2)
    mean_n = tables.Float32Col(pos=3)
    max_n = tables.UInt16Col(pos=4)
    min_signal = tables.UInt16Col(pos=5)
    mean_signal = tables.Float32Col(pos=6)
    max_signal = tables.UInt16Col(pos=7)


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
    altitude = tables.Float64Col(pos=10)
    temperature_inside = tables.BoolCol(pos=11)
    temperature_outside = tables.BoolCol(pos=12)
    humidity_inside = tables.BoolCol(pos=13)
    humidity_outside = tables.BoolCol(pos=14)
    barometer = tables.BoolCol(pos=15)
    wind_direction = tables.BoolCol(pos=16)
    wind_speed = tables.BoolCol(pos=17)
    solar_radiation = tables.BoolCol(pos=18)
    uv_index = tables.BoolCol(pos=19)
    evapotranspiration = tables.BoolCol(pos=20)
    rain_rate = tables.BoolCol(pos=21)
    heat_index = tables.BoolCol(pos=22)
    dew_point = tables.BoolCol(pos=23)
    wind_chill = tables.BoolCol(pos=24)
    offset_inside_temperature = tables.Float32Col(pos=25)
    offset_outside_temperature = tables.Float32Col(pos=26)
    offset_inside_humidity = tables.Int16Col(pos=27)
    offset_outside_humidity = tables.Int16Col(pos=28)
    offset_wind_direction = tables.Int16Col(pos=29)
    offset_station_altitude = tables.Float32Col(pos=30)
    offset_bar_sea_level = tables.Float32Col(pos=31)


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
    com_port = tables.UInt8Col(pos=2)
    baud_rate = tables.Int16Col(pos=3)
    station_id = tables.UInt32Col(pos=4)
    database_name = tables.Int32Col(dflt=-1, pos=5)
    help_url = tables.Int32Col(dflt=-1, pos=6)
    daq_mode = tables.BoolCol(pos=7)
    latitude = tables.Float64Col(pos=8)
    longitude = tables.Float64Col(pos=9)
    altitude = tables.Float64Col(pos=10)
    squelch_seting = tables.Int32Col(pos=11)
    close_alarm_distance = tables.Int32Col(pos=12)
    severe_alarm_distance = tables.Int32Col(pos=13)
    noise_beep = tables.BoolCol(pos=14)
    minimum_gps_speed = tables.Int32Col(pos=15)
    angle_correction = tables.Float32Col(pos=16)


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
    directory = data_dir / f'{date.year}/{date.month}'
    file = directory / f'{date.year}_{date.month}_{date.day}.h5'

    # Ensure dir and parent directories exist with mode rwxr-xr-x
    directory.mkdir(mode=0o755, parents=True, exist_ok=True)

    return tables.open_file(file, 'a')


def get_or_create_station_group(file, cluster, station_id):
    """Get an existing station group or create a new one

    :param file: the PyTables data file
    :param cluster: the name of the cluster
    :param station_id: the station number

    """
    cluster = get_or_create_cluster_group(file, cluster)
    node_name = f'station_{station_id}'
    try:
        station = file.get_node(cluster, node_name)
    except tables.NoSuchNodeError:
        station = file.create_group(cluster, node_name, f'HiSPARC station {station_id} data')
        file.flush()

    return station


def get_or_create_cluster_group(file, cluster):
    """Get an existing cluster group or create a new one

    :param file: the PyTables data file
    :param cluster: the name of the cluster

    """
    try:
        hisparc = file.get_node('/', 'hisparc')
    except tables.NoSuchNodeError:
        hisparc = file.create_group('/', 'hisparc', 'HiSPARC data')
        file.flush()

    node_name = 'cluster_' + cluster.lower()
    try:
        cluster = file.get_node(hisparc, node_name)
    except tables.NoSuchNodeError:
        cluster = file.create_group(hisparc, node_name, f'HiSPARC cluster {cluster} data')
        file.flush()

    return cluster


def get_or_create_node(file, cluster, node):
    """Get an existing node or create a new one

    :param file: the PyTables data file
    :param cluster: the parent (cluster) node
    :param node: the node (e.g. events, blobs)

    """
    try:
        node = file.get_node(cluster, node)
    except tables.NoSuchNodeError:
        if node == 'events':
            node = file.create_table(cluster, 'events', HisparcEvent, 'HiSPARC event data')
        elif node == 'errors':
            node = file.create_table(cluster, 'errors', HisparcError, 'HiSPARC error messages')
        elif node == 'config':
            node = file.create_table(cluster, 'config', HisparcConfiguration, 'HiSPARC configuration messages')
        elif node == 'comparator':
            node = file.create_table(cluster, 'comparator', HisparcComparator, 'HiSPARC comparator messages')
        elif node == 'singles':
            node = file.create_table(cluster, 'singles', HisparcSingle, 'HiSPARC single messages')
        elif node == 'satellites':
            node = file.create_table(cluster, 'satellites', HisparcSatellite, 'HiSPARC satellite messages')
        elif node == 'blobs':
            node = file.create_vlarray(cluster, 'blobs', tables.VLStringAtom(), 'HiSPARC binary data')
        elif node == 'weather':
            node = file.create_table(cluster, 'weather', WeatherEvent, 'HiSPARC weather data')
        elif node == 'weather_errors':
            node = file.create_table(cluster, 'weather_errors', WeatherError, 'HiSPARC weather error messages')
        elif node == 'weather_config':
            node = file.create_table(cluster, 'weather_config', WeatherConfig, 'HiSPARC weather configuration messages')
        elif node == 'lightning':
            node = file.create_table(cluster, 'lightning', LightningEvent, 'HiSPARC lightning data')
        elif node == 'lightning_errors':
            node = file.create_table(cluster, 'lightning_errors', LightningError, 'HiSPARC lightning error messages')
        elif node == 'lightning_config':
            node = file.create_table(
                cluster,
                'lightning_config',
                LightningConfig,
                'HiSPARC lightning configuration messages',
            )
        elif node == 'lightning_status':
            node = file.create_table(cluster, 'lightning_status', LightningStatus, 'HiSPARC lightning status messages')
        elif node == 'lightning_noise':
            node = file.create_table(cluster, 'lightning_noise', LightningNoise, 'HiSPARC lightning noise messages')
        file.flush()

    return node
