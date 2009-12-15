import datetime
from DEF.definesHdf5 import *
from DEF.definities import *
from DEF.rcodesHdf5 import *
from DEF.LockMechanism import *
from os import makedirs, access, F_OK, path
from fcntl import *
from tables import *
import time

global h5file, dummy

while(True):
	[h5file, dummy] = open_h5_file( datetime.date(2009,9,24), "r")
	print datetime.date(2009,9,23)
	var = raw_input("Press enter to unlock file ")
	close_flush_and_unlock(h5file, dummy)
	time.sleep(4)



