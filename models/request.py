from __future__ import annotations
from dataclasses import dataclass


@dataclass
class Request:
    request_id: int
    status: int                     # 0 - открыта, 1 - закрыта
    client_id: int
    operator_id: int | None
    comment: str | None
    rate: int | None
    client_login: str | None = None     # служебные поля, в таблице их нет
    operator_login: str | None = None
    status_text: str | None = None
