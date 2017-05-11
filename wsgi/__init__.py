"""
HiSPARC datastore WSGI application

This WSGI app is served by uWSGI on frome and lives at ``http://frome.nikef.nl/hisparc/upload``.

example ``application.wsgi``:

.. include:: ../examples/application.wsgi
   :literal:

configuration is read from a configuation file, shared between the WSGI app
and the writer usually `config.ini`:

.. include:: ../examples/config.ini
   :literal:

"""
