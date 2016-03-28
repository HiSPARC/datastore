# Rewrite configs that contain bad values

## 160222 - Rewriting old (broken) PySPARC configurations

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
        migrate_configs(102, 'amsterdam', (2015, 10, 19), (2016, 2, 16))
        migrate_configs(202, 'amsterdam', (2015, 10, 30), (2016, 2, 17))
        migrate_configs(599, 'amsterdam', (2015, 10, 19), (2016, 2, 17))


## 160304 - Convert mV thresholds to ADC for baseline at 30 ADC counts

A baseline of 200 ADC counts is used for HiSPARC II electronics. For a long
time the same baseline was used for HiSPARC III because of bugs in the DAQ.
These bugs are since resolved and the new LabView DAQ uses a baseline of 30 ADC
counts for HiSPARC III. However, the thresholds were ('are' for stations
running the old software) reported in mV. This has been changed to ADC counts
for stations running the new DAQ. Station 501 was used to test the new DAQ, and
worked for a time without the Monitor being updated to send thresholds in ADC
counts. So for some time it ran with a baseline of 30 but reported thresholds
as mV. This resulted in many events with failed trigger time reconstruction.
This script will convert the values in the affected configs to ADC counts and
with the correct baseline.

This affects station 501 from 2015-05-13 up to 2015-11-24 16:00.

    import datetime
    import os.path

    import tables


    def daterange(start, stop):
        t = datetime.date(*start)
        stop = datetime.date(*stop)

        while t < stop:
            yield t
            t += datetime.timedelta(days=1)


    def mv_to_adc(mv):
        return int(mv / -0.584 + 30)


    def migrate_configs(station, cluster, start, stop):
        thresholds = ['mas_ch1_thres_low', 'mas_ch1_thres_high',
                      'mas_ch2_thres_low', 'mas_ch2_thres_high',
                      'slv_ch1_thres_low', 'slv_ch1_thres_high',
                      'slv_ch2_thres_low', 'slv_ch2_thres_high']
        node_path = '/hisparc/cluster_%s/station_%d' % (cluster, station)
        for date in daterange(start, stop):
            path = date.strftime('/databases/frome/%Y/%-m/%Y_%-m_%-d.h5')
            with tables.open_file(path, 'a') as data:
                if node_path not in data:
                    continue
                node = data.get_node(node_path)
                if 'config' not in node:
                    continue
                print date
                for row in node.config:
                    for threshold in thresholds:
                        if row[threshold] < 0:
                            row[threshold] = mv_to_adc(row[threshold])
                    row.update()


    if __name__ == '__main__':
        migrate_configs(501, 'amsterdam', (2015, 5, 13), (2015, 11, 25))


Station 502 is also affected in two configs, one contains the 'correct' mV
value, but relative to the 200 ADC baseline. The second seems to contain the
wrong threshold values. For both all thresholds will be set to 200 ADC counts.

    PATH=/data/hisparc/env/miniconda/bin:$PATH
    source activate hisparc
    ipython
    %cpaste
    import tables

    thresholds = ['mas_ch1_thres_low', 'mas_ch1_thres_high',
                  'mas_ch2_thres_low', 'mas_ch2_thres_high',
                  'slv_ch1_thres_low', 'slv_ch1_thres_high',
                  'slv_ch2_thres_low', 'slv_ch2_thres_high']
    node_path = '/hisparc/cluster_amsterdam/station_502'
    paths = ['/databases/frome/2012/6/2012_6_8.h5',
             '/databases/frome/2012/7/2012_7_30.h5']
    for path in paths:
        with tables.open_file(path, 'a') as data:
            node = data.get_node(node_path)
            for row in node.config:
                for threshold in thresholds:
                    row[threshold] = 200
                row.update()
    --
