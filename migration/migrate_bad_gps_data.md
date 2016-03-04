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

