from os import makedirs, access, F_OK, path
import fcntl
import datetime
from definesHdf5 import *
import tables
from storage_layoutHdf5 import initialize_database
import logging

log_fhandler = logging.FileHandler("/tmp/hisparc_uploadLOCKING")
formatter = logging.Formatter("%(asctime)s %(levelname)s %(name)s:%(message)s")
log_fhandler.setFormatter(formatter)
logger = logging.getLogger()
logger.name = "main"
logger.addHandler(log_fhandler)
logger.setLevel(logging.INFO)


def close_flush_and_unlock(h5file, dummyFile):
    h5file.flush()
    h5file.close()
    logger.info("UNLOCKING `%s' " % (dummyFile))
    fcntl.lockf(dummyFile, fcntl.LOCK_UN)
    dummyFile.close()

def open_h5_file(date, mode):
    path= DATA_ROOT_DIR+"/%s/%s/" % (date.year, date.month)
    filename="%s_%s_%s.h5" % (date.year, date.month,date.day)

    try:
        makedirs(path,0777)
    except:
        pass

    #test if the H5 file actually exists
    if(not access(path+filename,F_OK)):
        initialize_database(path+filename)

    #We use a dummy file to lock the actual file
    logger.info("TRYING TO OPEN `%s'" % (path+filename))
    dummyFile = open(path+filename, mode)
    logger.info("LOCKING `%s'" % (path+filename))
    fcntl.lockf(dummyFile, fcntl.LOCK_EX)
    #Now once the file is locked, we open the h5handler
    logger.info("OPENING `%s'" % (path+filename))
    h5handler = tables.openFile(path+filename,mode)
    return [h5handler, dummyFile]
