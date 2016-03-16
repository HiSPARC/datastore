# Removed corrupted data for several stations

The event/trace data for several stations for 2012/11/5 are corrupted.
Attempts to read the data result in HDF5 read errors.

This corruption is seen for the following stations:
10, 303, 504, 1003, 2201, 3103, 3302, 7001, 8003, 8004, and 8006.

The following script is used to remove data for those stations on that date.
That way they wont interfere with the creation of the ESD.
Not only events but also some errors and weather data (station 8006) is removed.

    PATH=/data/hisparc/env/miniconda/bin:$PATH
    source activate hisparc
    ipython
    %cpaste
    import tables
    from sapphire import Station
    stations = [10, 303, 504, 1003, 2201, 3103, 3302, 7001, 8003, 8004, 8006]
    clusters = [Station(s).cluster().lower() for s in stations]
    with tables.open_file('/databases/frome/2012/11/2012_11_5.h5', 'a') as data:
        for station, cluster in zip(stations, clusters):
            data.remove_node('/hisparc/cluster_%s' % cluster, 'station_%d' % station, recursive=True)
    --



%cpaste
from django_publicdb.histograms.models import Summary, NetworkSummary
import datetime as dt
 
DATE = dt.date(2012, 11, 5)
summaries = Summary.objects.filter(date=DATE)
summaries.delete()
networksummary = NetworkSummary.objects.get(date=DATE)
networksummary.delete()
--
