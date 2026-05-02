from common.response import Response
from common.constants import Status


def write(path: str, data: bytes | str) -> Response:
    try:
        with open(path, "w" if isinstance(data, str) else "wb") as file:
            file.write(data)
    except PermissionError:
        return Response(Status.META_PERMISSION_DENIED, "Permission denied by the host OS.")
    except FileNotFoundError:
        return Response(Status.NOT_FOUND, f"Directory doesn't exist for {path}.")
    except IsADirectoryError:
        return Response(Status.ERROR, f"{path} is a directory.")
    except OSError:
        return Response(Status.EXTSYS_ERROR, f"External Error.")
    return Response(Status.SUCCESS, f"Successfully written in the file {path}.")


def read(path: str, data_type: type[bytes | str]) -> Response:
    try:
        with open(path, "r" if data_type is str else "rb") as file:
            read_data = file.read()
    except PermissionError:
        return Response(Status.META_PERMISSION_DENIED, "Permission denied by the host OS.")
    except FileNotFoundError:
        return Response(Status.NOT_FOUND, f"{path} could not be found.")
    except IsADirectoryError:
        return Response(Status.ERROR, f"{path} is a directory.")
    except OSError:
        return Response(Status.EXTSYS_ERROR, "External Error.")
    return Response(Status.SUCCESS, f"Successfully read from {path}.", data=read_data)