"""Wrapper for the writer application"""

import sys

sys.path.append('/var/www/wsgi-bin/datastore/')

from writer import writer_app

configfile = '/var/www/wsgi-bin/datastore/examples/config.ini'
writer_app.writer(configfile)
