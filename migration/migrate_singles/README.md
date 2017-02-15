HisparcSingle ('/singles' in the datastore ) colomns where `tables.UInt16Col`
before HiSPARC/datastore@dec64079 (merged feb 12, 2017, after this migration).
For stations without a slave (two detector stations) the slave columns where
set to all zero, instead of all `-1` to represent 'missing sensor'.

In this migration all datastore '/singles' tables where converted to the new
format (`tables.Int32Col`: signed 32bit integers). The original tables are kept
in the datastore files as '/singles_old'.

After stopping the datastore writer, all affected datastore files were copied:

tkooij@frome:
```
screen
cp -var /databases/frome/2016/ /data/hisparc/backup_datastore_13feb2017/
cp -var /databases/frome/2017/ /data/hisparc/backup_datastore_13feb2017/
```

conda env for frome with pytables-3.3.0 and up to date sapphire:
tkooij@login:

```
conda create -n frome python=2.7 ipython numpy scipy pytables
pip install hisparc-sapphire
```

Migrate:
root@frome:
```
screen
PATH=/data/hisparc/env/miniconda/bin:$PATH
source activate frome
python migrate_singles.py
```

Afterwards the writer was started.


This resulting migration.log was commited in this folder.

Errors from `migration.log` are shown below. Stations 91, 93 and 1102 are test
stations. Station 1102 is staged to become an active station in the Utrecht
cluster, but the affected data is test data.

The error message states that there was no information about the station in
the API. As a result, the station was treated as a 4 detector station and
slave columns were not changed from 0 to -1. As station 1102 is a 4 detector
station (with slave) this is not a problem.

```
2017-02-13 19:34:59,238 - ERROR - No information in HiSPARCNetwork() for sn 91
2017-02-13 19:44:07,376 - ERROR - No information in HiSPARCNetwork() for sn 93
2017-02-13 19:46:22,919 - ERROR - No information in HiSPARCNetwork() for sn 1102
```
