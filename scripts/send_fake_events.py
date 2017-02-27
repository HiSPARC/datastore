import datetime
import random
import time

import numpy as np

import pysparc.events
import pysparc.storage


class FakeMessage(object):

    datetime = datetime.datetime.now()
    timestamp = time.time()
    nanoseconds = int(random.uniform(0, 1e9))
    ext_timestamp = int(timestamp) * int(1e9) + nanoseconds
    trigger_pattern = 1
    trace_ch1 = np.arange(10)
    trace_ch2 = np.arange(10)


datastore = pysparc.storage.NikhefDataStore(99, 'fake_station',
                                            url='http://localhost:8083')
for i in range(100):
    event = pysparc.events.Event(FakeMessage())
    datastore.store_event(event)
