from __future__ import annotations
from database.database import get_connection
from models.request import Request

# логины клиента и оператора берём из таблицы User
SELECT_SQL = """
    SELECT r.RequestID, r.status, r.clientID, r.operatorID, r.comment, r.rate,
           c.login, o.login
    FROM Request r
    JOIN User c ON c.UserID = r.clientID
    LEFT JOIN User o ON o.UserID = r.operatorID
"""


def _map(row) -> Request:
    req = Request(*row)
    # текстовый статус считаем сами
    if req.status == 1:
        req.status_text = "Закрыта"
    elif req.operator_id is None:
        req.status_text = "Новая"
    else:
        req.status_text = "В работе"
    return req


def create(client_id: int, comment: str):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("INSERT INTO Request(status, clientID, comment) VALUES (0, ?, ?)",
                (client_id, comment))
    conn.commit()
    conn.close()


def get_by_id(request_id: int) -> Request | None:
    conn = get_connection()
    cur = conn.cursor()
    cur.execute(SELECT_SQL + " WHERE r.RequestID = ?", (request_id,))
    row = cur.fetchone()
    conn.close()
    return _map(row) if row else None


def get_all() -> list[Request]:
    conn = get_connection()
    cur = conn.cursor()
    cur.execute(SELECT_SQL + " ORDER BY r.RequestID")
    rows = cur.fetchall()
    conn.close()
    return [_map(r) for r in rows]


def get_by_client(client_id: int) -> list[Request]:
    conn = get_connection()
    cur = conn.cursor()
    cur.execute(SELECT_SQL + " WHERE r.clientID = ? ORDER BY r.RequestID", (client_id,))
    rows = cur.fetchall()
    conn.close()
    return [_map(r) for r in rows]


def take(request_id: int, operator_id: int):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("UPDATE Request SET operatorID = ? WHERE RequestID = ?",
                (operator_id, request_id))
    conn.commit()
    conn.close()


def close(request_id: int):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("UPDATE Request SET status = 1 WHERE RequestID = ?", (request_id,))
    conn.commit()
    conn.close()


def set_rate(request_id: int, rate: int):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("UPDATE Request SET rate = ? WHERE RequestID = ?", (rate, request_id))
    conn.commit()
    conn.close()


def update_comment(request_id: int, comment: str):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("UPDATE Request SET comment = ? WHERE RequestID = ?",
                (comment, request_id))
    conn.commit()
    conn.close()


def delete(request_id: int):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("DELETE FROM Request WHERE RequestID = ?", (request_id,))
    conn.commit()
    conn.close()
