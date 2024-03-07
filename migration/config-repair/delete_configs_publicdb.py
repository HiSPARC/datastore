"""
delete (incorrect) configuration from publicdb database

delete all configurations from (STATION, DATE). Set num_config in summary
"""
import os
import sys

from datetime import date


STATION = 91
DATE = date(2017, 4, 12)

print('removing all configs for sn %d at %s' % (STATION, DATE))

PUBLICDB_PATH = '/srv/publicdb/www'
sys.path.append(PUBLICDB_PATH)

os.environ['DJANGO_SETTINGS_MODULE'] = 'publicdb.settings'

import django
django.setup()

from publicdb.histograms.models import Summary, Configuration


summary = Summary.objects.get(station__number=STATION, date=DATE)
assert summary.station.number == STATION
assert summary.date == DATE
print(summary.station)
print(summary)

configs = Configuration.objects.filter(source=summary)
print('n = ', configs.count())

for i, config in enumerate(configs.iterator()):
    if not i % 1000:
        print(i, config)
    config.delete()

n_configs = Configuration.objects.filter(source=summary).count()
print('after delete: n = ', n_configs)
summary.num_config = n_configs
summary.save()
