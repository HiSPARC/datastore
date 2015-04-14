eventtype_upload_codes = {
    'CIC': {
        '_tablename': 'events',
        '_blobs': ['TR'],
        '_has_ext_time': True,
        'RED': 'data_reduction',
        'EVENTRATE': 'event_rate',
        'TRIGPATTERN': 'trigger_pattern',
        'BL': 'baseline',
        'STDDEV': 'std_dev',
        'NP': 'n_peaks',
        'PH': 'pulseheights',
        'IN': 'integrals',
        'TR': 'traces',
    },
    'ERR': {
        '_tablename': 'errors',
        '_blobs': ['ERRMSG'],
        '_has_ext_time': False,
        'ERRMSG': 'messages',
    },
    'CFG': {
        '_tablename': 'config',
        '_blobs': ['CFG_MAS_VERSION', 'CFG_SLV_VERSION', 'CFG_PASSWORD',
                   'CFG_BUFFER'],
        '_has_ext_time': False,
        'CFG_GPS_LAT': 'gps_latitude',
        'CFG_GPS_LONG': 'gps_longitude',
        'CFG_GPS_ALT': 'gps_altitude',
        'CFG_MAS_VERSION': 'mas_version',
        'CFG_SLV_VERSION': 'slv_version',
        'CFG_TRIGLOWSIG': 'trig_low_signals',
        'CFG_TRIGHIGHSIG': 'trig_high_signals',
        'CFG_TRIGEXT': 'trig_external',
        'CFG_TRIGANDOR': 'trig_and_or',
        'CFG_PRECTIME': 'precoinctime',
        'CFG_CTIME': 'coinctime',
        'CFG_POSTCTIME': 'postcoinctime',
        'CFG_DETNUM': 'detnum',
        'CFG_PASSWORD': 'password',
        'CFG_SPAREBYTES': 'spare_bytes',
        'CFG_USEFILTER': 'use_filter',
        'CFG_USEFILTTHRES': 'use_filter_threshold',
        'CFG_REDUCE': 'reduce_data',
        'CFG_BUFFER': 'buffer',
        'CFG_STARTMODE': 'startmode',
        'CFG_DELAYSCREEN': 'delay_screen',
        'CFG_DELAYCHECK': 'delay_check',
        'CFG_DELAYERROR': 'delay_error',
        'CFG_MAS_CH1THRLOW': 'mas_ch1_thres_low',
        'CFG_MAS_CH1THRHIGH': 'mas_ch1_thres_high',
        'CFG_MAS_CH2THRLOW': 'mas_ch2_thres_low',
        'CFG_MAS_CH2THRHIGH': 'mas_ch2_thres_high',
        'CFG_MAS_CH1INTTIME': 'mas_ch1_inttime',
        'CFG_MAS_CH2INTTIME': 'mas_ch2_inttime',
        'CFG_MAS_CH1VOLT': 'mas_ch1_voltage',
        'CFG_MAS_CH2VOLT': 'mas_ch2_voltage',
        'CFG_MAS_CH1CURR': 'mas_ch1_current',
        'CFG_MAS_CH2CURR': 'mas_ch2_current',
        'CFG_MAS_COMPTHRLOW': 'mas_comp_thres_low',
        'CFG_MAS_COMPTHRHIGH': 'mas_comp_thres_high',
        'CFG_MAS_MAXVOLT': 'mas_max_voltage',
        'CFG_MAS_RESET': 'mas_reset',
        'CFG_MAS_CH1GAINPOS': 'mas_ch1_gain_pos',
        'CFG_MAS_CH1GAINNEG': 'mas_ch1_gain_neg',
        'CFG_MAS_CH2GAINPOS': 'mas_ch2_gain_pos',
        'CFG_MAS_CH2GAINNEG': 'mas_ch2_gain_neg',
        'CFG_MAS_CH1OFFPOS': 'mas_ch1_offset_pos',
        'CFG_MAS_CH1OFFNEG': 'mas_ch1_offset_neg',
        'CFG_MAS_CH2OFFPOS': 'mas_ch2_offset_pos',
        'CFG_MAS_CH2OFFNEG': 'mas_ch2_offset_neg',
        'CFG_MAS_COMMOFF': 'mas_common_offset',
        'CFG_MAS_INTVOLTAGE': 'mas_internal_voltage',
        'CFG_MAS_CH1ADCGAIN': 'mas_ch1_adc_gain',
        'CFG_MAS_CH1ADCOFF': 'mas_ch1_adc_offset',
        'CFG_MAS_CH2ADCGAIN': 'mas_ch2_adc_gain',
        'CFG_MAS_CH2ADCOFF': 'mas_ch2_adc_offset',
        'CFG_MAS_CH1COMPGAIN': 'mas_ch1_comp_gain',
        'CFG_MAS_CH1COMPOFF': 'mas_ch1_comp_offset',
        'CFG_MAS_CH2COMPGAIN': 'mas_ch2_comp_gain',
        'CFG_MAS_CH2COMPOFF': 'mas_ch2_comp_offset',
        'CFG_SLV_CH1THRLOW': 'slv_ch1_thres_low',
        'CFG_SLV_CH1THRHIGH': 'slv_ch1_thres_high',
        'CFG_SLV_CH2THRLOW': 'slv_ch2_thres_low',
        'CFG_SLV_CH2THRHIGH': 'slv_ch2_thres_high',
        'CFG_SLV_CH1INTTIME': 'slv_ch1_inttime',
        'CFG_SLV_CH2INTTIME': 'slv_ch2_inttime',
        'CFG_SLV_CH1VOLT': 'slv_ch1_voltage',
        'CFG_SLV_CH2VOLT': 'slv_ch2_voltage',
        'CFG_SLV_CH1CURR': 'slv_ch1_current',
        'CFG_SLV_CH2CURR': 'slv_ch2_current',
        'CFG_SLV_COMPTHRLOW': 'slv_comp_thres_low',
        'CFG_SLV_COMPTHRHIGH': 'slv_comp_thres_high',
        'CFG_SLV_MAXVOLT': 'slv_max_voltage',
        'CFG_SLV_RESET': 'slv_reset',
        'CFG_SLV_CH1GAINPOS': 'slv_ch1_gain_pos',
        'CFG_SLV_CH1GAINNEG': 'slv_ch1_gain_neg',
        'CFG_SLV_CH2GAINPOS': 'slv_ch2_gain_pos',
        'CFG_SLV_CH2GAINNEG': 'slv_ch2_gain_neg',
        'CFG_SLV_CH1OFFPOS': 'slv_ch1_offset_pos',
        'CFG_SLV_CH1OFFNEG': 'slv_ch1_offset_neg',
        'CFG_SLV_CH2OFFPOS': 'slv_ch2_offset_pos',
        'CFG_SLV_CH2OFFNEG': 'slv_ch2_offset_neg',
        'CFG_SLV_COMMOFF': 'slv_common_offset',
        'CFG_SLV_INTVOLTAGE': 'slv_internal_voltage',
        'CFG_SLV_CH1ADCGAIN': 'slv_ch1_adc_gain',
        'CFG_SLV_CH1ADCOFF': 'slv_ch1_adc_offset',
        'CFG_SLV_CH2ADCGAIN': 'slv_ch2_adc_gain',
        'CFG_SLV_CH2ADCOFF': 'slv_ch2_adc_offset',
        'CFG_SLV_CH1COMPGAIN': 'slv_ch1_comp_gain',
        'CFG_SLV_CH1COMPOFF': 'slv_ch1_comp_offset',
        'CFG_SLV_CH2COMPGAIN': 'slv_ch2_comp_gain',
        'CFG_SLV_CH2COMPOFF': 'slv_ch2_comp_offset',
    },
    'CMP': {
        '_tablename': 'comparator',
        '_blobs': [],
        '_has_ext_time': True,
        'CMP_DEVICE': 'device',
        'CMP_COMPARATOR': 'comparator',
        'CMP_COUNT': 'count',
    },
    'WTR': {
        '_tablename': 'weather',
        '_blobs': [],
        '_has_ext_time': False,
        'WTR_TEMP_INSIDE': 'temp_inside',
        'WTR_TEMP_OUTSIDE': 'temp_outside',
        'WTR_HUMIDITY_INSIDE': 'humidity_inside',
        'WTR_HUMIDITY_OUTSIDE': 'humidity_outside',
        'WTR_BAROMETER': 'barometer',
        'WTR_WIND_DIR': 'wind_dir',
        'WTR_WIND_SPEED': 'wind_speed',
        'WTR_SOLAR_RAD': 'solar_rad',
        'WTR_UV': 'uv',
        'WTR_ET': 'evapotranspiration',
        'WTR_RAIN_RATE': 'rain_rate',
        'WTR_HEAT_INDEX': 'heat_index',
        'WTR_DEW_POINT': 'dew_point',
        'WTR_WIND_CHILL': 'wind_chill',
    },
    'WER': {
        '_tablename': 'weather_errors',
        '_blobs': ['WER_ERRMSG'],
        '_has_ext_time': False,
        'WER_ERRMSG': 'messages',
    },
    'WCG': {
        '_tablename': 'weather_config',
        '_blobs': ['WCG_HELP_URL', 'WCG_DATABASE_NAME'],
        '_has_ext_time': False,
        'WCG_COM_PORT': 'com_port',
        'WCG_BAUD_RATE': 'baud_rate',
        'WCG_STATION_ID': 'station_id',
        'WCG_DATABASE_NAME': 'database_name',
        'WCG_HELP_URL': 'help_url',
        'WCG_DAQ_MODE': 'daq_mod',
        'WCG_LATITUDE': 'latitude',
        'WCG_LONGITUDE': 'longitude',
        'WCG_ALTITUDE':, 'altitude',
        'WCG_TEMPERATURE_INSIDE': 'temperature_inside',
        'WCG_TEMPERATURE_OUTSIDE': 'temperature_outside',
        'WCG_HUMIDITY_INSIDE': 'humidity_inside',
        'WCG_HUMIDITY_OUTSIDE': 'humidity_outside',
        'WCG_BAROMETER': 'barometer',
        'WCG_WIND_DIRECTION': 'wind_direction',
        'WCG_WIND_SPEED': 'wind_speed',
        'WCG_SOLAR_RADIATION': 'solar_radiation',
        'WCG_UV_INDEX': 'uv_index',
        'WCG_EVAPOTRANSPIRATION': 'evapotranspiration',
        'WCG_RAIN_RATE': 'rain_rate',
        'WCG_HEAT_INDEX': 'heat_index',
        'WCG_DEW_POINT': 'dew_point',
        'WCG_WIND_CHILL': 'wind_chill',
        'WCG_OFFSET_INSIDE_TEMPERATURE': 'offset_inside_temperature',
        'WCG_OFFSET_OUTSIDE_TEMPERATURE': 'offset_outside_temperature',
        'WCG_OFFSET_INSIDE_HUMIDITY': 'offset_inside_humidity',
        'WCG_OFFSET_OUTSIDE_HUMIDITY': 'offset_outside_humidity',
        'WCG_OFFSET_WIND_DIRECTION': 'offset_wind_direction',
        'WCG_OFFSET_STATION_ALTITUDE':, 'offset_station_altitude',
        'WCG_OFFSET_BAR_SEA_LEVEL':, 'offset_bar_sea_level',
    },
    'LIT': {
        '_tablename': 'lightning',
        '_blobs': [],
        '_has_ext_time': False,
        'LIT_CORR_DIST': 'corr_distance',
        'LIT_UNCORR_DIST': 'uncorr_distance',
        'LIT_UNCORR_ANGLE': 'uncorr_anlge',
        'LIT_CORR_ANGLE': 'corr_anlge',
    },
    'LER': {
        '_tablename': 'lightning_errors',
        '_blobs': ['LER_ERRMSG'],
        '_has_ext_time': False,
        'LER_ERRMSG': 'messages',
    },
    'LCG': {
        '_tablename': 'lightning_config',
        '_blobs': ['LCG_HELP_URL','LCG_DATABASE_NAME'],
        '_has_ext_time': False,
        'LCG_COM_PORT': 'com_port',
        'LCG_BAUD_RATE': 'baud_rate',
        'LCG_STATION_ID': 'station_id',
        'LCG_DATABASE_NAME': 'database_name',
        'LCG_HELP_URL': 'help_url',
        'LCG_DAQ_MODE': 'daq_mode',
        'LCG_LATITUDE': 'latitude',
        'LCG_LONGITUDE': 'longitude',
        'LCG_ALTITUDE': 'altitude',
        'LCG_SQUELCH_SETTING': 'squelch_setting',
        'LCG_CLOSE_ALARM_DISTANCE': 'close_alarm_distance',
        'LCG_SEVERE_ALARM_DISTANCE': 'severe_alarm_distance',
        'LCG_NOISE_BEEP': 'noise_beep',
        'LCG_MINIMUM_GPS_SPEED': 'minimum_gps_speed',
        'LCG_ANGLE_CORRECTION': 'angle_correction',
    },
    'LST': {
        '_tablename': 'lightning_status',
        '_blobs': [],
        '_has_ext_time': False,
        'LST_CLOSE_RATE': 'close_rate',
        'LST_TOTAL_RATE': 'total_rate',
        'LST_CLOSE_ALARM': 'close_alarm',
        'LST_SEVERE_ALARM': 'severe_alarm',
        'LST_CURR_HEADING': 'current_heading',
    },
    'LNS': { # This is an empty message!
        '_tablename': 'lightning_noise',
        '_blobs': [],
        '_has_ext_time': False,
    },
}
