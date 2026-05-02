from enum import IntEnum

class Status(IntEnum):
    SUCCESS = 0
    ERROR = -1
    PERMISSION_DENIED = -2
    NOT_FOUND = -3
    META_PERMISSION_DENIED = -4 # Actual OS running this code denied
    EXTSYS_ERROR = -9
    UNREC_ERROR = -99
    FATAL_ERROR = -999

class Privilege(IntEnum):
    ADMIN = 0
    NONADMIN = 1
    KERNEL = 2