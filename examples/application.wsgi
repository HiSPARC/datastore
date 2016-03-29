import sys
import functools

sys.path.append('/var/www/wsgi-bin/datastore/wsgi')

import wsgi_app

configfile = '/var/www/wsgi-bin/datastore/examples/config.ini'
application = functools.partial(wsgi_app.application, configfile=configfile)
