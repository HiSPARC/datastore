# Migrate GPS test data to test stations

For a GPS offset test station 501 and 502 were triggered simultaneously
using a pulsegenerator. The data is poluting the real cosmic data. The
data is easily identified by the trace signals (no pulses, external
trigger) and the interval between events (250 ms). Moreover, we
performed the tests so we know the dates: From 2011/10/21 upto and
including 2011/10/31. We should move this data away from these stations
and store under test stations. Stations 94 and 95 are obvious
candidates, since those are used for similar tests and started data
taking after the 501-502 tests. We should ensure that 94/95 also recieve
configs from 501/502 to get the right gps coordinates.

See https://github.com/HiSPARC/datastore/issues/5


## Datastore
### frome has an older version of PyTables

    cd /databases/frome/2011/10/
    cp 2011_10_{21..31}.h5 /data/hisparc/adelaat/temp_data/

    PATH=/data/hisparc/env/miniconda/bin:$PATH
    source activate /data/hisparc/hisparc_env/

    ipython

    %cpaste
    import tables

    # 2011/10/21: Move config data from station 501/502 to 94/95
    with tables.open_file('2011_10_21.h5', 'a') as data:
        data.move_node(where='/hisparc/cluster_amsterdam/station_501',
                       newparent='/hisparc/cluster_amsterdam/station_94',
                       name='config', newname='config', createparents=True)
        data.move_node(where='/hisparc/cluster_amsterdam/station_502',
                       newparent='/hisparc/cluster_amsterdam/station_95',
                       name='config', newname='config', createparents=True)

    # 2011/10/21 & 2011/10/31: Remove event/errors/blob data from station 501/502 (keep weather)
    for day in [21, 31]:
        with tables.open_file('2011_10_%d.h5' % day, 'a') as data:
            for station in [501, 502]:
                for table in ['events', 'blobs', 'errors']:
                    try:
                        data.remove_node('/hisparc/cluster_amsterdam/station_%d' % station, table)
                    except tables.NoSuchNodeError:
                        pass

    # 2011/10/22 - 2011/10/30: Move data (events/blobs/configs/errors) from 501/502 to 94/95, leave weather data
    for day in range(22, 31):
        with tables.open_file('2011_10_%d.h5' % day, 'a') as data:
            data.move_node(where='/hisparc/cluster_amsterdam',
                           name='station_502', newname='station_95')
            for table in ['events', 'blobs', 'config', 'errors']:
                try:
                    data.move_node(where='/hisparc/cluster_amsterdam/station_501',
                                   newparent='/hisparc/cluster_amsterdam/station_94',
                                   name=table, createparents=True)
                except tables.NoSuchNodeError:
                    pass
    --


## Publicdb

    envpub
    cdpub
    cd django_publicdb
    ./manage.py shell

    %cpaste
    from datetime import date, timedelta

    from django_publicdb.inforecords.models import Station
    from django_publicdb.histograms.models import Summary, Configuration, NetworkSummary

    STARTDATE = date(2011, 10, 21)
    ENDDATE = date(2011, 11, 1)

    for number in [501, 502]:
        station = Station.objects.filter(number=number)
        # 2011/10/21 - 2011/10/31: Remove summaries from 501/502
        summaries = Summary.objects.filter(station=station,
                                           date__gte=STARTDATE, date__lt=ENDDATE)
        summaries.delete()
        # 2011/10/21 - 2011/10/30: Remove configurations from 501/502
        configs = Configuration.objects.filter(source__station=station,
                                               timestamp__gte=STARTDATE,
                                               timestamp__lt=ENDDATE)
        configs.delete()

    # 2011/10/21 - 2011/10/31: Flag network coincidences for update
    for n in range((ENDDATE - STARTDATE).days):
        d = STARTDATE + timedelta(days=n)
        n_sum = Summary.objects.filter(date=d, num_events__isnull=False,
                                       station__pc__is_test=False).count()
        if n_sum >= 2:
            network_summary, _ = NetworkSummary.objects.get_or_create(date=d)
            network_summary.needs_update = True
            network_summary.needs_update_coincidences = True
            network_summary.save()
    --


## ESD

    # 2011/10/21 - 2011/10/31: Remove ESD data for 501/502
    envpub
    cdpub
    cd esd/2011/10
    ipython

    %cpaste
    import tables

    for day in range(21, 32):
        with tables.open_file('2011_10_%d.h5' % day, 'a') as data:
            for station in [501, 502]:
                data.remove_node('/hisparc/cluster_amsterdam/station_%d' % station,
                                 recursive=True)
    --



## Forgot config blobs

    cd /databases/frome/2011/10/

    PATH=/data/hisparc/env/miniconda/bin:$PATH
    source activate /data/hisparc/hisparc_env/

    ipython

    %cpaste
    import tables

    with tables.open_file('2011_10_21.h5', 'a') as data:
        with tables.open_file('/data/hisparc/adelaat/temp_data/2011_10_21.h5', 'r') as data2:
            for s_from, s_to in [[501, 94], [502, 95]]:
                source = data2.get_node('/hisparc/cluster_amsterdam/station_%d' % s_from)
                target = data.get_node('/hisparc/cluster_amsterdam/station_%d' % s_to)
                data.create_vlarray(target, 'blobs', tables.VLStringAtom(),
                                    'HiSPARC binary data')

                m_idx = target.config[0]['mas_version']
                s_idx = target.config[0]['slv_version']

                target.blobs.append(source.blobs[m_idx])
                target.blobs.append(source.blobs[s_idx])

                target.config.modify_column(column=[0], colname='mas_version')
                target.config.modify_column(column=[1], colname='slv_version')

    with tables.open_file('2011_10_31.h5', 'a') as data:
        with tables.open_file('/data/hisparc/adelaat/temp_data/2011_10_31.h5', 'r') as data2:
            for station in [501, 502]:
                source = data2.get_node('/hisparc/cluster_amsterdam/station_%d' % station)
                target = data.get_node('/hisparc/cluster_amsterdam/station_%d' % station)
                data.create_vlarray(target, 'blobs', tables.VLStringAtom(),
                                    'HiSPARC binary data')

                m_idx = target.config[0]['mas_version']
                s_idx = target.config[0]['slv_version']

                target.blobs.append(source.blobs[m_idx])
                target.blobs.append(source.blobs[s_idx])

                target.config.modify_column(column=[0], colname='mas_version')
                target.config.modify_column(column=[1], colname='slv_version')

    --
