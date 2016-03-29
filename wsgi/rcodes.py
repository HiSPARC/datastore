"""
Return codes.
There are four types of return codes:
1. OK (100)
2. putEvent errors (20*)
3. getEvent errors (30*)
3. Internal server error (40*)
"""

RC_OK = 100  # OK, Everything went fine.

# putEvent
RC_PE_INV_INPUT = 201  # Wrong input
RC_PE_INV_UPCODE = 202  # Wrong upload code
RC_PE_INV_AUTHCODE = 203  # Wrong password
RC_PE_EVENT_EXISTS = 204  # Event already exists in de database.
RC_PE_TRANS_FAILED = 205  # Transaction failed
RC_PE_INV_STATIONID = 206  # Station Unknown
RC_PE_INV_EVENTTYPE = 207  # Wrong event type

# getEvent

# Internal server errors.
RC_ISE_INV_POSTDATA = 400  # HTTP Bad Request
RC_ISE_DB_CONNECT_FAILED = 404  # Database unreachable.
