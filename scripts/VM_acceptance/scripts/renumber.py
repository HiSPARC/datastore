"""
Renumber data from real stations to test stations
 station 501 -> station 99
 station 501 -> station 98
"""

FOLDER = 'pickles/'

def renumber_pickles(folder):
    """relabel pickles to station_id = 99"""
    files = glob.glob(os.path.join(folder, 'tmp*'))

    for fn in files:
        with open(fn, 'rb') as f:
            x = pickle.load(f)
        print(fn)
        if x['station_id'] == 501:
            s_id = 99
        elif x['station_id'] == 502:
            s_id = 98
        else:
            print('skip:', x['station_id'])
            continue
        data = {'station_id': 99, 'cluster': 'Amsterdam',
            'event_list': x['event_list']}
        with open(fn, 'wb') as f:
            pickle.dump(data, f)


if __name__ == '__main__':
    renumber_pickles(FOLDER)
