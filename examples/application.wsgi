import sys

sys.path.append('/home/david/work/HiSPARC/software/bzr/datastore')
sys.path.append('/home/david/work/HiSPARC/software/bzr/datastore/src')

import wsgi_app

application = wsgi_app.application
