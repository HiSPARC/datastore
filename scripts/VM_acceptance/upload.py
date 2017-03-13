"""
Upload folder to datastore VM

usage:

python upload.py folder_name

"""

import datetime
import hashlib
import requests
import glob
import os
import pickle
import sys

from sapphire.utils import pbar


DATASTORE_VM = 'http://192.168.99.13/nikhef/upload'

STATION_LIST = ((98, 'fake_station'), (99, 'fake_station'))


class Uploader(object):

    def __init__(self, url, station_list):
        self.url = url
        self.passwords = {}
        for sn, password in station_list:
            self.passwords[sn] = password
            assert sn in [98, 99], 'Do not use this on real data!'

    def upload(self, sn, eventlist):
        assert type(eventlist) is list, 'The data is not a list!'

        pickled_data = pickle.dumps(eventlist, protocol=0)
        return self._upload_data(sn, pickled_data)

    def _upload_data(self, sn, pickled_data, checksum=None):
        """Upload event data to wsgi-app.
        :param pickled_data: pickled event data (bytestring).
        :param checksum: optional checksum to send.
        returns the rcode or raises UploadError.
        """

        if checksum is None:
            checksum = hashlib.md5(pickled_data).hexdigest()

        payload = {'station_id': sn,
                   'password': self.passwords[sn],
                   'data': pickled_data.decode('iso-8859-1'),
                   'checksum': checksum}
        try:
            r = requests.post(self.url, data=payload, timeout=10)
            r.raise_for_status()
        except (ConnectionError) as exc:
            raise UploadError(str(exc))
        else:
            return r.text


class YieldPickles(object):
    """yield pickles from a folder"""

    def __init__(self, folder):
        self.files = glob.glob(os.path.join(folder, 'tmp*'))
        self.n = len(self.files)

    def __len__(self):
        return self.n

    def __iter__(self):
        for fn in self.files:
            with open(fn, 'rb') as f:
                data = pickle.load(f)
                yield data['station_id'], data['event_list']


if __name__ == '__main__':
    datastore = Uploader(DATASTORE_VM, STATION_LIST)

    folder_to_upload = sys.argv[1]
    pickles = YieldPickles(folder_to_upload)

    print('Uploading %d pickles from folder: %s' % (len(pickles),
                                                    folder_to_upload))
    for sn, event_list in pbar(pickles):
        assert sn in [98, 99]
        try:
            r = datastore.upload(sn, event_list)
        except Exception as exc:
            print('Connection failed: ', str(exc))
            break
        if r != '100':
            print('Datastore responded with errorcoded: ', r, type(r))
            break
