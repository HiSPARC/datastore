from os import makedirs, access, F_OK, path
from fcntl import *
import datetime
from definesHdf5 import *
from tables import *
from storage_layoutHdf5 import initialize_database
import logging

log_fhandler = logging.FileHandler("/tmp/hisparc_uploadLOCKING")
formatter = logging.Formatter("%(asctime)s %(levelname)s %(name)s:%(message)s")
log_fhandler.setFormatter(formatter)
logger = logging.getLogger()logger.name = "main"
logger.addHandler(log_fhandler)
logger.setLevel(logging.INFO)



def close_flush_and_unlock(h5file, dummyFile):
    print "\nWE ARE GOING TO CLOSE " , dummyFile
    h5file.flush()
    h5file.close()
    print "\tUNLOCKING %s" % (dummyFile)
    logger.info("UNLOCKING `%s' " % (dummyFile))
    flock(dummyFile, LOCK_UN)
    dummyFile.close()
    print "\tFILE CLOSE AND UNLOCKED"



def open_h5_file(date, mode):
    path= DATA_ROOT_DIR+"/%s/%s/" % (date.year, date.month)
    filename="%s_%s_%s.h5" % (date.year, date.month,date.day)

    print "We are currently trying to open file : %s/%s" % (path, filename)

    try:
            makedirs(path,0777)
    except:
            print "directory %s already exists" % path
    #test if the H5 file actually exists
    if(not access(path+filename,F_OK)):
            initialize_database(path+filename)
            print"file %s/%s was created" % (path,filename)

    #We use a dummy file to lock the actual file
    print "\nTRYING TO OPEN ", path+filename
    logger.info("TRYING TO OPEN `%s'" % (path+filename))
    dummyFile = open(path+filename, mode)
    print "\tLOCKING %s" % (path+filename)
    logger.info("LOCKING `%s'" % (path+filename))
    flock(dummyFile, LOCK_EX)
    #Now once the file is locked, we open the h5handler
    print "\tOPENING ", path+filename
    logger.info("OPENING `%s'" % (path+filename))
    h5handler = openFile(path+filename,mode)
    return [h5handler, dummyFile]
