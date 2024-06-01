Acceptance test for a datastore VM

Prerequisites:
 - A datastore VM
 - A collection of pickles uploaded by a real station and a matching
   datastore HDF5 file.
   At nikhef a full day of station 501 is available.
   The data is in the test_data/ folder.

Usage:

Prepare VM. Edit upload.py to match VM.

$ python upload.py test_data/station_99

Wait for the writer to finish on the VM. Copy the 2017_3_2.h5 datastore file
to the folder that contains `expected_2017_3_2.h5`

$ python compare.py
