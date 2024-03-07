DATASTORE_PATH = '/databases/frome'
STATION_LIST = '/databases/frome/station_list.csv'
OLDDB_STATUS = '/databases/frome/migration-olddb-status'
EWH_STATUS = '/databases/frome/migration-status'
BATCHSIZE = 1000

OLDDB_HOST = 'oust'
OLDDB_USER = 'webread'
OLDDB_DB = 'hisparc'
OLDDB_PORT = 3306

EWH_HOST = 'peene'
EWH_USER = 'analysis'
EWH_PASSWD = 'Data4analysis!'
EWH_DB = 'eventwarehouse'
EWH_PORT = 3306

renumbered_stations = {
    1: 501,
    4: 101,
    8: 301,
    11: 302,
    12: 303,
    14: 304,
    15: 509,
    16: 201,
    17: 401,
    18: 402,
    19: 501,
    20: 202,
    23: 601,
    24: 102,
    601: 99999,  # KASCADE
    3004: 3301,
    3005: 3302,
    3006: 3303,
    6001: 20001,
    7010: 7101,
    7020: 7201,
    7030: 7301,
    7300: 7301,
    8002: 8101,
    8003: 8201,
    8008: 8102,
    8009: 8103,
    8010: 8002,
    8011: 8104,
    8012: 8003,
    8013: 8301,
    8014: 8302,
    8015: 8303,
}
