import os

from typing import Callable
from functools import partial

from common.constants import Status, Privilege, _BOOT_FILES
from common.response import Response
from common.user import User
from core import file_handler, crypt


_log_type = Callable[[str], None] | None
_KERNEL_FILEPATH = os.path.join("disk", "kernel")
_USERS: list[User] = []
_SECRET_KEY: bytes = b""

def _load_secret_key() -> Response:
    global _SECRET_KEY
    fernet_path = os.path.join(_KERNEL_FILEPATH, _BOOT_FILES.SECRET_INFO)
    res = file_handler.read(fernet_path, bytes)

    if res.status != Status.SUCCESS:
        return res

    if not (isinstance(res.data, bytes) and crypt.validate_key(res.data)):
        return Response(Status.UNREC_ERROR, "Secret is corrupted.", data=res.data)

    _SECRET_KEY = res.data
    return Response(Status.SUCCESS, "Secret was loaded.")


def _load_users(log: _log_type = None):
    user_path = os.path.join(_KERNEL_FILEPATH, _BOOT_FILES.USER_TABLE)
    raw_data = file_handler.read(user_path, bytes).data
    # TODO


def boot(log: _log_type = None) -> Response:
    _pfr = partial(factory_reset, privilege = Privilege.KERNEL)

    if log: log("Boot process started.")
    if not os.path.isdir(_KERNEL_FILEPATH):
        return Response(Status.UNREC_ERROR, "Boot folder could not be found.", _pfr)

    if log: log("Boot folder found.")
    for file in _BOOT_FILES:
        path = os.path.join(_KERNEL_FILEPATH, file)
        if not os.path.isfile(path):
            return Response(Status.UNREC_ERROR, f"{file} could not be found.", _pfr)

    if log: log("Boot files found.")
    res = _load_secret_key()
    if res.status == Status.UNREC_ERROR:
        return Response(Status.UNREC_ERROR, res.message, _pfr)
    elif res.status != Status.SUCCESS:
        return res
    
    return Response(Status.SUCCESS, "Successfully booted.")


def factory_reset(log: _log_type = None, privilege: Privilege = Privilege.NONADMIN) -> Response:
    
    def create_file(path: str) -> None:
        os.makedirs(os.path.dirname(path), exist_ok=True)
        with open(path, "w"): pass
    
    if privilege == Privilege.NONADMIN:
        return Response(Status.PERMISSION_DENIED, "Non-admin users can not do a factory reset.")

    # Create boot folder
    if os.path.isdir(_KERNEL_FILEPATH):
        for file in _BOOT_FILES:
            path = os.path.join(_KERNEL_FILEPATH, file)
            if os.path.isfile(path):
                os.remove(path)
                if log: log(f"Removed {file}")
    
    # Create boot files
    for file in _BOOT_FILES:
        path = os.path.join(_KERNEL_FILEPATH, file)
        create_file(path)
        if log: log(f"Created {file}")
    
    # Generate secret key
    key = crypt.generate_new_key()
    fernet_path = os.path.join(_KERNEL_FILEPATH, _BOOT_FILES.SECRET_INFO)
    res = file_handler.write(fernet_path, key)
    if res.status != Status.SUCCESS:
        return res
    
    return Response(Status.SUCCESS, "Factory reset was successful")


def create_user(user: User, password: str, log: _log_type = None, privilege: Privilege = Privilege.NONADMIN) -> Response:
    
    return Response(Status.SUCCESS, f"{user.username} created successfully.")