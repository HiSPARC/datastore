import sys
import functools

sys.path.append('/home/david/work/HiSPARC/software/bzr/datastore/wsgi')

configfile = ('/home/david/work/HiSPARC/software/bzr/datastore/examples'
              '/config.ini')

import wsgi_app
application = functools.partial(wsgi_app.application,
                                configfile=configfile)
