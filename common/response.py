from dataclasses import dataclass
from typing import Callable
from common.constants import Status

@dataclass
class Response:
    status: Status
    message: str
    next: Callable | None = None
    data: dict | bytes | str | None = None