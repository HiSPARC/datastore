eventtype_upload_codes = {
    'CIC': {
        'tablename': 'events',
        'blobs': ['TR'],
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
        'tablename': 'errors',
        'blobs': ['ERRMSG'],
        'ERRMSG': 'messages',
    },
    'CMP': {
        'tablename': 'comparator',
        'blobs': [],
        'CMP_DEVICE': 'device',
        'CMP_COMPARATOR': 'comparator',
        'CMP_COUNT': 'count',
    },
}
