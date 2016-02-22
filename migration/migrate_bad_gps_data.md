# Migrate wrong GPS config data to test stations

## Determining which Configurations to move

### 502 and 506

From 506 GPS csv:

    1264778223 -51.699101325 -152.947194382
    1264778249 -51.63778044 -152.924936433
    1265846400 -51.63778044 -152.924936433
    1305202040 0.367904958508 -0.901326636664
    ...

All configs between 1264778223 up to and not including 1305202040
2010, 1, 29, 15, 17, 3  --  2011, 5, 12, 12, 7, 20

    Configuration.objects.filter(source__station__number=506,
                                 timestamp__gte=datetime(2010, 1, 29, 15, 17, 3),
                                 timestamp__lt=datetime(2011, 5, 12, 12, 7, 20))
    # [<Configuration: 506 - 2010-01-29 15:17:03>, <Configuration: 506 - 2010-01-29 15:17:29>,
    #  <Configuration: 506 - 2010-01-29 15:43:59>, <Configuration: 506 - 2010-01-29 16:49:55>]


From 502 GPS csv:

    1262249784 71.5800871772 70.9049809869
    1264171486 0.803975970685 0.311570197873
    ...

All configs between 1262249784 up to and not including 1264171486
2009, 12, 31, 8, 56, 24  --  2010, 1, 22, 14, 44, 46

    Configuration.objects.filter(source__station__number=502,
                                 timestamp__gte=datetime(2009, 12, 31, 8, 56, 24),
                                 timestamp__lt=datetime(2010, 1, 22, 14, 44, 46))
    # [<Configuration: 502 - 2009-12-31 08:56:24>, <Configuration: 502 - 2010-01-03 21:04:23>,
    #  <Configuration: 502 - 2010-01-04 15:48:27>]


It turns out these configs were not in the data files (possibly removed
before?). So I removed the counter from the Summaries and deleted the
Configurations.


### 503

From GPS csv:

    ...
    1339065700 0.0 0.0
    1348659099 -128.437173431 -54.69000788
    1353324606 0.0 0.0
    ...

All configs between 1348659099 up to and not including 1353324606
2012, 9, 26, 11, 31, 39  --  2012, 11, 19, 11, 30, 6

    Configuration.objects.filter(source__station__number=503,
                                 timestamp__gte=datetime(2012, 9, 26, 11, 31, 39),
                                 timestamp__lt=datetime(2012, 11, 19, 11, 30, 6))
    # [<Configuration: 503 - 2012-09-26 11:31:39>]

Since this is only one config, and known to be from a simple test,
it will be removed from the raw data.


#### Remove specific config

The blobs will remain untouched, to prevent having to fix all the event
trace references. The config node, containing only the one config, will
be removed.

    PATH=/data/hisparc/env/miniconda/bin:$PATH
    source activate hisparc

    ipython

    %cpaste
    import tables
    with tables.open_file('/databases/frome/2012/9/2012_9_26.h5', 'a') as data:
        data.remove_node('/hisparc/cluster_amsterdam/station_503', 'config')
    --


### Configurations to be removed for 507

No config in raw data for (2010, 2, 16). Remove the configs for the other
dates with bad gps data.

    PATH=/data/hisparc/env/miniconda/bin:$PATH
    source activate hisparc

    ipython

    %cpaste
    import tables
    d = [(1999, 8, 22), (2010, 3, 15), (2010, 3, 16),
         (2010, 6, 4), (2010, 6, 11), (2012, 11, 21), (2012, 12, 20)]
    for yy, mm, dd in d:
        print yy, mm, dd
        path = '/databases/frome/{yy}/{mm}/{yy}_{mm}_{dd}.h5'.format(yy=yy, mm=mm, dd=dd)
        with tables.open_file(path, 'a') as data:
            data.remove_node('/hisparc/cluster_amsterdam/station_507', 'config')
        print 'removed config'
    --


### 151203 - More configurations to remove

For each station I retrieved all GPS locations and determined the distances
between each pair of consecutive locations. In cases where this was more
than 250 meters I investigated if this was correct or a mistake.
For stations 22, 301, 2010, 4003, and 13001 I found bad locations.
Often caused by required troubleshooting with the station PC at Nikhef.
And once a close but not exactly (0., 0., 0.) locations.

These bad configs, and in some cases also the test data from a pulse
generator, have been removed.

22 - 2015-10-29/30
301 - 2014-12-2
2010 - 2012-6-8
4003 - 2014-4-2
13001 - 2013-7-10


### 160222 - Rewriting old (broken) PySPARC configurations

The old implementation of config messages were broken for PySPARC stations. We
fixed that, but had to rewrite the raw configurations in the data files. We
used the following script:

    import datetime
    import os.path

    import tables


    VERSION = "Hardware: 0 FPGA: 0"


    def daterange(start, stop):
        t = datetime.date(*start)
        stop = datetime.date(*stop)

        while t < stop:
            yield t
            t += datetime.timedelta(days=1)


    def migrate_configs(station, cluster, start, stop):
        for date in daterange(start, stop):
            path = '/databases/frome/{yy}/{mm}/{yy}_{mm}_{dd}.h5'.format(
                yy=date.year, mm=date.month, dd=date.day)
            print date
            with tables.open_file(path, 'a') as f:
                node = '/hisparc/cluster_%s/station_%d' % (cluster, station)
                if node not in f:
                    continue
                node = f.get_node(node)
                if 'config' not in node:
                    continue
                for row in node.config:
                    if row['coinctime'] > 100:
                        row['coinctime'] /= 1000.
                    if row['precoinctime'] > 100:
                        row['precoinctime'] /= 1000.
                    if row['postcoinctime'] > 100:
                        row['postcoinctime'] /= 1000.
                    if row['mas_ch1_current'] > 25.:
                        row['mas_ch1_current'] *= (25. / 0xff)
                    if row['mas_ch2_current'] > 25.:
                        row['mas_ch2_current'] *= (25. / 0xff)
                    idx = row['slv_version']
                    version = node.blobs[idx]
                    if version != VERSION:
                        node.blobs.append(VERSION)
                        idx = len(node.blobs) - 1
                        row['slv_version'] = idx
                    row['trig_low_signals'] = 2
                    row.update()
                if len(node.config) > 10.:
                    node.config.truncate(10)


    if __name__ == '__main__':
        migrate_configs(102, 'amsterdam', (2015, 10, 22), (2016, 2, 16))
        migrate_configs(202, 'amsterdam', (2015, 10, 30), (2016, 2, 17))
        migrate_configs(599, 'amsterdam', (2015, 10, 22), (2016, 2, 17))
