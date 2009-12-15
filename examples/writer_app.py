"""Wrapper for the writer application"""

import sys

sys.path.append('/home/david/work/HiSPARC/software/bzr/datastore/writer')

import writer

configfile = ('/home/david/work/HiSPARC/software/bzr/datastore/examples'
              '/config.ini')
writer.writer(configfile)
