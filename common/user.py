from dataclasses import dataclass
from common.constants import Privilege

@dataclass
class User:
    username: str
    privilege: Privilege