from enum import IntEnum

class Status(IntEnum):
    SUCCESS = 0
    FATAL_ERROR = -1
    PERMISSION_DENIED = -2
    NOT_FOUND = -3
    UNREC_ERROR = -99

class Privilege(IntEnum):
    ADMIN = 0
    NONADMIN = 1
    KERNEL = 2