import datetime
import random

import numpy as np
import pysparc.events
import pysparc.storage

from sapphire import datetime_to_gps


class FakeMessage:
    def __init__(self, dt=datetime.datetime.now()):
        self.datetime = dt
        self.timestamp = datetime_to_gps(dt)
        self.nanoseconds = int(random.uniform(0, 1e9))
        self.ext_timestamp = int(self.timestamp) * int(1e9) + self.nanoseconds
        self.trigger_pattern = 1
        self.trace_ch1 = np.arange(10)
        self.trace_ch2 = np.arange(10)


VM = 'http://localhost:8083/nikhef/upload'
datastore = pysparc.storage.NikhefDataStore(99, 'fake_station', url=VM)

for d in range(1, 10):
    event = pysparc.events.Event(FakeMessage(dt=datetime.datetime(2019, 4, d)))
    datastore.store_event(event)
