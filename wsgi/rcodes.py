"""
Return codes for the WSGI app.

There are four types of return codes:

1. OK (100)
2. putEvent errors (20*)

   - 201: invalid input: checksum of data does not match
   - 203: wrong password
   - 206: station unknown (check ``station-list.csv``)
   - 208: unpickling error

3. getEvent errors (30*)

   not used by WSGI app

4. Internal server error (40*)

   - 400: internal server error. Invalid post data.
"""

RC_OK = b'100'  # OK, Everything went fine.

# putEvent
RC_PE_INV_INPUT = b'201'  # Wrong input
RC_PE_INV_UPCODE = b'202'  # Wrong upload code
RC_PE_INV_AUTHCODE = b'203'  # Wrong password
RC_PE_EVENT_EXISTS = b'204'  # Event already exists in de database.
RC_PE_TRANS_FAILED = b'205'  # Transaction failed
RC_PE_INV_STATIONID = b'206'  # Station Unknown
RC_PE_INV_EVENTTYPE = b'207'  # Wrong event type
RC_PE_PICKLING_ERROR = b'208'  # unpickle failed

# Internal server errors.
RC_ISE_INV_POSTDATA = b'400'  # HTTP Bad Request
RC_ISE_DB_CONNECT_FAILED = b'404'  # Database unreachable.
