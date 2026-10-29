from __future__ import annotations
from dataclasses import dataclass


@dataclass
class User:
    user_id: int
    login: str
    password_hash: str
    user_role_id: int
    role_name: str | None = None    # служебное поле, в таблице его нет
