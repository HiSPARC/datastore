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
        migrate_configs(102, 'amsterdam', (2015, 10, 22), (2016, 2, 16))
        migrate_configs(202, 'amsterdam', (2015, 10, 30), (2016, 2, 17))
        migrate_configs(599, 'amsterdam', (2015, 10, 22), (2016, 2, 17))
