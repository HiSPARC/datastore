"""Migrate KASCADE station data

This is the final version that was run to do the migration

"""

import datetime
import os

import tables

START_DATE = datetime.date(2010, 12, 1)
TRANSISTION_DATE = datetime.date(2011, 1, 7)
END_DATE = datetime.date(2011, 11, 27)
DATASTORE_PATH = '/databases/frome/'


def migrate():
    """Migrate HiSPARC KASCADE station data to new number and cluster

    Before the transisition date (7-1-2011) the KASCADE station was in
    the cluster 'kascade', on this date it was changed to cluster
    amsterdam. It also used to have station number 701 This does not
    work well with our numbering methods.

    It has been decided to fix this and put the station in the country
    Germany (70000) and thus rename the station to 70001 and put
    it back in the kascade cluster.

    This script will move the data in the datastore files to the new
    location. A third of the data on the transisition date is ignored.

    """
    date = START_DATE

    while date < END_DATE:
        path = DATASTORE_PATH + date.strftime('%Y/%-m/%Y_%-m_%-d.h5')
        if os.path.isfile(path):
            file = tables.openFile(path, 'a')
            try:
                print(f'Found data file for {date.isoformat()}...')
                if date >= TRANSISTION_DATE:
                    # After transistion date data will be in cluster amsterdam
                    # Move and rename the node
                    node = file.root.hisparc.cluster_amsterdam.station_701
                    print('moving data..')
                    try:
                        target = file.root.hisparc.cluster_karlsruhe
                    except tables.NoSuchNodeError:
                        target = file.createGroup(
                            '/hisparc',
                            'cluster_karlsruhe',
                            'HiSPARC cluster Karlsruhe data',
                            createparents=True,
                        )
                    node._f_move(newparent=target, newname='station_70001')
                    print('done.')
                else:
                    # Before transition date data already in cluster karlsruhe
                    # Only rename the node
                    node = file.root.hisparc.cluster_karlsruhe.station_701
                    print('moving data..')
                    node._f_rename('station_70001')
                    print('done.')
            except tables.NoSuchNodeError:
                print('no data group to move.')
            file.close()
        else:
            print(f'No data file for {date.isoformat()}.')

        date += datetime.timedelta(days=1)


if __name__ == '__main__':
    migrate()
