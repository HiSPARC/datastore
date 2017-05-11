"""
HiSPARC datastore writer application

This script polls ``/datatore/frome/incoming`` for incoming data written
by the WSGI app. It then writes the data into the raw datastore.

example ``writer_app.py``:

.. include:: ../examples/writer_app.py
   :literal:

configuration is read from a configuation file, shared between the WSGI app
and the writer usually `config.ini`:

.. include:: ../examples/config.ini
   :literal:
"""
