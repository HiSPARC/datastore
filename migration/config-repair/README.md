# Repair/remove incorrect config data stations 508, 4 and 91

Due to a bug in a new version of the HiSPARC DAQ enormous amounts of configuration states were sent to the datastore. Luckily this new version was only installed at stations 508, 4 and 91. The first row of the configuration table is correct so all other rows can be removed. This will be done once an improved version of the DAQ is installed at all affected stations. The problem arose on 12-04-2017 for station 91, on 15-04-2017 and 16-04-2017 for station 4 and on 18-04-2017 for station 508. Note that the blobs are also affected. Removing the config blob data entries would mean that other blob indexes need to be updated as well, so it is decided to simply leave that data.

See https://github.com/HiSPARC/datastore/issues/23

For the datastore the remove_incorrect_configs.py script can be used.

Note that the raw data is stored at /databases/frome (accesible via frome), that the ESD data is stored at /srv/publicdb/www/esd/ (accesible via pique) and that the publicdb database is located at /var/run/postgresql.


## Datastore
### frome has an older version of PyTables (version 2.1.2)

    cd /databases/frome/2011/10/
    cp 2017_4_{days_affected}.h5 /data/hisparc/kaspervd/temp_data/

    # Possibly needed to work with python on frome
    PATH=/data/hisparc/env/miniconda/bin:$PATH
    source activate /data/hisparc/hisparc_env/

    # Edit the script to include all days with incorrect config data
    ipython remove_incorrect_configs.py

The following configs were deleted from the data store (on 2017-jul-7):

    sn 91, 2017-4-12
    sn 4, 2017-4-15
    sn 4, 2017-4-16
    sn 508, 2017-4-18

Backups of the original files are available at /data/hisparc/kaspervd/config-fix-data

## Publicdb

Incorrect configs from the publicdb database were removed using the script:
`delete_configs_publicdb.py` ::

    ssh hisparc@pique
    envpub
    wget <url of delete_configs_publicdb.py --> github>
    vim delete_configs_publicdb.py
    python delete_configs_publicdb.py

The following configs were deleted (on 2017-apr-21):

    sn 91, 2017-4-12
    sn 4, 2017-4-15
    sn 4, 2017-4-16
    sn 508, 2017-4-18
