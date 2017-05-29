This dataset is (very) large: About 200 Mb LZMA compressed.
It is not committed to our git repositories. At Nikhef, it can be found at:
/data/hisparc/datastore_acceptance_test/



This is real data from station 501 captured on March 2nd, 2017.
The data is renumber to station 99 to prevent problems if it accidentally gets
uploaded to the real datastore.

All datafiles (pickles) are in the `station_99/` folder.

The matching datastore file is: `expected_2017_3_2.h5`.

It was copied from the real datastore using `ptrepack`:

```
$ scp hisparc@pique:/databases/frome/2017/3/2017_3_2.h5 .
$ ptrepack 2017_3_2.h5:/hisparc/cluster_amsterdam/station_501 expected_2017_3_2.h5:/hisparc/cluster_amsterdam/station_99
```

Contents:
```
expected_2017_3_2.h5 (File) ''
Last modif.: 'Mon May 29 11:15:04 2017'
Object Tree:
/ (RootGroup) ''
/hisparc (Group) 'HiSPARC data'
/hisparc/cluster_amsterdam (Group) 'HiSPARC cluster amsterdam data'
/hisparc/cluster_amsterdam/station_99 (Group) 'HiSPARC station 99 data'
/hisparc/cluster_amsterdam/station_99/blobs (VLArray(240223,)) 'HiSPARC binary data'
/hisparc/cluster_amsterdam/station_99/config (Table(1,)) 'HiSPARC configuration messages'
/hisparc/cluster_amsterdam/station_99/events (Table(60055,)) 'HiSPARC event data'
/hisparc/cluster_amsterdam/station_99/satellites (Table(24,)) 'HiSPARC satellite messages'
/hisparc/cluster_amsterdam/station_99/singles (Table(84601,)) 'HiSPARC single messages'
/hisparc/cluster_amsterdam/station_99/weather (Table(16822,)) 'HiSPARC weather data'
```
