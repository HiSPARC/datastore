import sys
# This script creates the file system to store hdf5 data files
# 
# file system
#   year
#     | 
#   month
#	  |
#   day-of-month
#     |
#   hisparc ... weather ... 
#     |
#   HDF5 file

__author__="prmarcu"
__date__ ="$18-sep-2009"

import os
import tables
import definesHdf5
import fcntl import



# init some parameters
startYear = 2009
endYear = 2009	
numMonths = 12
numDays = 31


'''
Removes HDF5 file location from the given base directory.
RFemoves all the files starting from year startYear until and inclusive
year endYear
'''
#def removeHdf5Files(databaseDir, startYear, endYear):
#	# remove if the file existed
#	if os.path.isdir("./" + databaseDir + "/"):
#		os.chdir(databaseDir)
#		for year in range(startYear, endYear+1):
#			for month in range(1, numMonths+1):
#				for day in range(1, numDays+1):
#					filePath = "./" + str(year) + "/" + str(month) + "/" + str(day) + "/" + defines.DATAFILE
#					if os.path.isfile(filePath):
#						os.remove(filePath)
#						print "Remove file %s ...DONE!" % (filePath)
#		os.chdir("..")
#	print "Remove files...DONE!"




# goto the coresponding directory
'''
Changes the directory to the specified location
Note: in HDF5 location is characterized by year month day
'''
def changeDir(year, month):
	sPath = definesHdf5.STORAGEDIR + str(year) + "/" + str(month) + "/" 
	if os.path.isdir(sPath):
		os.chdir(sPath)
		print "Current working directory: %s" % (sPath)
	else:
		print "Cannot find path: %s" % (sPath)

#-------- End of openDir function----------#
'''
   Opens the  HDF5 data file to be used with pytables
   NOTE: uses the STORAGEDIR constant from the definesHdf5 file.
'''
def openDataFile(year, month, day, mode):
	#sPath = "./" + defines.DATA_ROOT_DIR + "/" + str(year) + "/" + str(month) + "/" + str(year)+"_"+str(month)+"_"+str(day)+"h5"
        sPath = definesHdf5.STORAGEDIR+str(year) + "/" + str(month) + "/" + str(year)+"_"+str(month)+"_"+str(day)+".h5"
	print "Open data file: %s" % (sPath)
	try:
		dataFile = tables.openFile(sPath, mode)
		#print dataFile
                return dataFile
	except IOError:
		print "Cannot open file: %s" % (sPath)
                #sys.exit(1)

'''
Opens the data file specified by the path.
@param path- the path to the HDF5 file
@param mode- the opening mode of the file (r, a+ etc)

@return - the pyTable file object
'''
def openDataFilePath(path,mode):
    print "Open data file: %s" % (path)
    try:
		dataFile = tables.openFile(path, mode)
		#print dataFile
                return dataFile
    except IOError:
		print "Cannot open file: %s" % (path)
                #sys.exit(1)


'''
Opens and locks a dummy file. usefull for file locking.
Since the filelocking on the HDF5 file doesn't work well

@return - the file descriptor of the locked file

'''
def openAndLockDummyFile():
    #open the file
    fileDescriptor=open(definesHdf5.DUMMY_FILENAME,"a")

    #lock the file
    fcntl.flock(fileDescriptor, fcntl.LOCK_EX)

    #return the file descriptor
    return fileDescriptor


'''
Unlocks and closes the dummy file.
@param fileDescriptor - the filedescriptor of the locked dummy file.
'''
def unlockAndCloseDummyFile(fileDescriptor):
    #unlock the dummy file
    fcntl.flock(fileDescriptor, fcntl.LOCK_UN)

    #close the file
    fileDescriptor.close()
