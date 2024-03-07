#!/usr/local/bin/python
""" Simple XML-RPC Server to run on the datastore server.

This daemon should be run on HiSPARC's datastore server.  It will
handle the cluster layouts and station passwords.  When an update is
necessary, it will reload the HTTP daemon.

The basis for this code was ripped from the python SimpleXMLRPCServer
library documentation and extended.

"""
import urllib.request, urllib.error, urllib.parse
import hashlib
import subprocess
import os

from xmlrpc.server import SimpleXMLRPCServer
from xmlrpc.server import SimpleXMLRPCRequestHandler

HASH = '/tmp/hash_datastore'
DATASTORE_CFG = '/databases/frome/station_list.csv'
CFG_URL = 'http://192.168.99.11/config/datastore'
DATASTORE_XMLRPC_SERVER = ('192.168.99.13', 8001)
RELOAD_PATH = '/tmp/uwsgi-reload.me'


def reload_datastore():
    """Load datastore config and reload datastore, if necessary"""

    datastore_cfg = urllib.request.urlopen(CFG_URL).read()
    new_hash = hashlib.sha1(datastore_cfg).hexdigest()

    try:
        with open(HASH, 'r') as file:
            old_hash = file.readline()
    except IOError:
        old_hash = None

    if new_hash == old_hash:
        return True
    else:
        with open(DATASTORE_CFG, 'w') as file:
            file.write(datastore_cfg)

        # reload uWSGI
        with open(RELOAD_PATH, 'a'):
            os.utime(RELOAD_PATH, None)

        with open(HASH, 'w') as file:
            file.write(new_hash)

    return True


if __name__ == '__main__':
    # Restrict to a particular path.
    class RequestHandler(SimpleXMLRPCRequestHandler):
        rpc_paths = ('/RPC2',)

    # Create server
    server = SimpleXMLRPCServer(DATASTORE_XMLRPC_SERVER,
                                requestHandler=RequestHandler)
    server.register_introspection_functions()

    server.register_function(reload_datastore)

    # Run the server's main loop
    server.serve_forever()
