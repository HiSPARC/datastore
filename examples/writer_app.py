"""Wrapper for the writer application"""

import sys

sys.path.append('/var/www/wsgi-bin/datastore/writer')

import writer

configfile = '/var/www/wsgi-bin/datastore/examples/config.ini'
writer.writer(configfile)
