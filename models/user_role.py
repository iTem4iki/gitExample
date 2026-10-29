from __future__ import annotations
from dataclasses import dataclass

CLIENT_ROLE_ID = 1
OPERATOR_ROLE_ID = 2


@dataclass
class UserRole:
    user_role_id: int
    name: str
    description: str | None = None
