import os

from typing import Callable
from functools import partial
from dataclasses import dataclass

from common.constants import Status, Privilege


_log_type = Callable[[str], None] | None
_KERNEL_FILEPATH = os.path.join("disk", "kernel")
_BOOT_FILES = ["filetable", "sysinfo", "secretinfo", "usertable"]


@dataclass
class Response:
    status: Status
    message: str
    data: Callable | None = None


def boot(log: _log_type = None) -> Response:
    if log: log("Boot process started.")
    if not os.path.isdir(_KERNEL_FILEPATH):
        return Response(Status.UNREC_ERROR, "Boot folder could not be found.", partial(factory_reset, privilege = Privilege.KERNEL))

    if log: log("Boot folder found.")
    for file in _BOOT_FILES:
        path = os.path.join(_KERNEL_FILEPATH, file)
        if not os.path.isfile(path):
            return Response(Status.UNREC_ERROR, f"{file} could not be found.", partial(factory_reset, privilege = Privilege.KERNEL))

    if log: log("Boot files found.")
    return Response(Status.SUCCESS, "Successfully booted.")


def factory_reset(log: _log_type = None, privilege: Privilege = Privilege.NONADMIN) -> Response:
    
    def create_file(path: str) -> None:
        os.makedirs(os.path.dirname(path), exist_ok=True)
        with open(path, "w"): pass
    
    if privilege == Privilege.NONADMIN:
        return Response(Status.PERMISSION_DENIED, "Non-admin users can not do a factory reset.")

    if os.path.isdir(_KERNEL_FILEPATH):
        for file in _BOOT_FILES:
            path = os.path.join(_KERNEL_FILEPATH, file)
            if os.path.isfile(path):
                os.remove(path)
                if log: log(f"Removed {file}")

    for file in _BOOT_FILES:
        path = os.path.join(_KERNEL_FILEPATH, file)
        create_file(path)
        if log: log(f"Created {file}")
    
    return Response(Status.SUCCESS, "Factory reset was successful")